#!/usr/bin/env python3
"""
Complete BigCommerce Data Downloader
Downloads ALL product images, variants, pricing rules, and categories
"""

import requests
import json
import os
import urllib.request
import time
from pathlib import Path
import sys
from concurrent.futures import ThreadPoolExecutor
import threading

class CompleteDownloader:
    def __init__(self, store_hash, access_token, client_id):
        self.store_hash = store_hash
        self.access_token = access_token
        self.client_id = client_id
        self.base_url = f"https://api.bigcommerce.com/stores/{store_hash}/v3"
        self.headers = {
            'X-Auth-Token': access_token,
            'X-Auth-Client': client_id,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        # Create directories
        self.data_dir = Path('data')
        self.images_dir = Path('images')
        self.data_dir.mkdir(exist_ok=True)
        self.images_dir.mkdir(exist_ok=True)
        (self.images_dir / 'products').mkdir(exist_ok=True)
        (self.images_dir / 'categories').mkdir(exist_ok=True)
        (self.images_dir / 'variants').mkdir(exist_ok=True)
        
        self.download_stats = {
            'products': 0,
            'categories': 0,
            'images': 0,
            'variants': 0,
            'pricing_rules': 0
        }
        self.lock = threading.Lock()

    def make_request(self, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            time.sleep(0.03)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"ERROR: {e}")
            return None

    def download_image(self, url, filename):
        if not url:
            return None
        try:
            filepath = self.images_dir / filename
            if filepath.exists():
                return str(filepath)
            urllib.request.urlretrieve(url, filepath)
            with self.lock:
                self.download_stats['images'] += 1
            return str(filepath)
        except Exception as e:
            return None

    def download_complete_products(self):
        print("STARTING COMPLETE MUNCHMAKERS DOWNLOAD")
        print("=" * 60)
        
        # Get total counts first
        products_info = self.make_request('/catalog/products', {'limit': 1})
        categories_info = self.make_request('/catalog/categories', {'limit': 1})
        
        if not products_info or not categories_info:
            print("Failed to connect to BigCommerce API")
            return
        
        total_products = products_info.get('meta', {}).get('pagination', {}).get('total', 0)
        total_categories = categories_info.get('meta', {}).get('pagination', {}).get('total', 0)
        
        print(f"TOTAL TO DOWNLOAD:")
        print(f"  Products: {total_products}")
        print(f"  Categories: {total_categories}")
        print(f"  Estimated Images: {total_products * 3 + total_categories} (~400-1000)")
        print()
        
        # Download categories first
        print("STEP 1: DOWNLOADING CATEGORIES...")
        categories = self.fetch_all_categories()
        
        print(f"\nSTEP 2: DOWNLOADING ALL PRODUCTS...")
        products = self.fetch_all_products_complete()
        
        print(f"\nSTEP 3: DOWNLOADING ALL PRODUCT IMAGES...")
        self.download_all_product_images(products)
        
        print(f"\nSTEP 4: DOWNLOADING VARIANTS AND PRICING...")
        self.fetch_variants_and_pricing(products)
        
        # Final save
        self.save_final_data(products, categories)
        
        print("\nDOWNLOAD COMPLETE!")
        print("=" * 60)
        print(f"FINAL STATS:")
        print(f"  Products: {self.download_stats['products']}")
        print(f"  Categories: {self.download_stats['categories']}")
        print(f"  Images Downloaded: {self.download_stats['images']}")
        print(f"  Variants: {self.download_stats['variants']}")
        print(f"  Pricing Rules: {self.download_stats['pricing_rules']}")

    def fetch_all_categories(self):
        categories = []
        page = 1
        
        while True:
            print(f"Categories page {page}...", end=" ")
            data = self.make_request('/catalog/categories', {'page': page, 'limit': 250})
            if not data or not data.get('data'):
                break
            
            for category in data['data']:
                # Download category image
                if category.get('image_url'):
                    filename = f"categories/cat_{category['id']}.jpg"
                    local_path = self.download_image(category['image_url'], filename)
                    category['local_image_path'] = local_path
                
                categories.append(category)
                self.download_stats['categories'] += 1
            
            print(f"Downloaded {len(data['data'])} categories")
            
            if page >= data.get('meta', {}).get('pagination', {}).get('total_pages', 1):
                break
            page += 1
        
        return categories

    def fetch_all_products_complete(self):
        products = []
        page = 1
        
        while True:
            print(f"Products page {page}...", end=" ")
            
            data = self.make_request('/catalog/products', {
                'page': page, 
                'limit': 50,
                'include': 'images,variants,custom_fields,bulk_pricing_rules,primary_image'
            })
            
            if not data or not data.get('data'):
                break
            
            for product in data['data']:
                self.download_stats['products'] += 1
                progress = (self.download_stats['products'] / 137) * 100
                print(f"\r{self.download_stats['products']}/137 ({progress:.1f}%) {product['name'][:40]}...", end="")
                
                products.append(product)
            
            if page >= data.get('meta', {}).get('pagination', {}).get('total_pages', 1):
                break
            page += 1
        
        print(f"\nProducts downloaded: {len(products)}")
        return products

    def download_all_product_images(self, products):
        print("Downloading ALL product images...")
        
        for i, product in enumerate(products):
            print(f"Product {i+1}/{len(products)}: {product['name'][:30]}...")
            
            # Download primary image
            if product.get('primary_image') and product['primary_image'].get('url_zoom'):
                filename = f"products/prod_{product['id']}_main.jpg"
                local_path = self.download_image(product['primary_image']['url_zoom'], filename)
                product['primary_image']['local_path'] = local_path
            
            # Download all product images
            product['all_images'] = []
            images_data = self.make_request(f'/catalog/products/{product["id"]}/images')
            if images_data and images_data.get('data'):
                for j, img in enumerate(images_data['data']):
                    # Download zoom image
                    if img.get('url_zoom'):
                        filename = f"products/prod_{product['id']}_img_{j}.jpg"
                        local_path = self.download_image(img['url_zoom'], filename)
                        img['local_path'] = local_path
                        product['all_images'].append(img)
                        
                        print(f"  Downloaded image {j+1}/{len(images_data['data'])}")

    def fetch_variants_and_pricing(self, products):
        print("Fetching variants and pricing rules...")
        
        for i, product in enumerate(products):
            print(f"Product {i+1}/{len(products)}: Getting variants/pricing...")
            
            # Fetch variants
            variants_data = self.make_request(f'/catalog/products/{product["id"]}/variants')
            if variants_data and variants_data.get('data'):
                product['variants'] = variants_data['data']
                self.download_stats['variants'] += len(variants_data['data'])
                
                # Download variant images
                for variant in product['variants']:
                    if variant.get('image_url'):
                        filename = f"variants/var_{variant['id']}.jpg"
                        local_path = self.download_image(variant['image_url'], filename)
                        variant['local_image_path'] = local_path
            
            # Fetch bulk pricing rules
            pricing_data = self.make_request(f'/catalog/products/{product["id"]}/bulk-pricing-rules')
            if pricing_data and pricing_data.get('data'):
                product['pricing_rules'] = pricing_data['data']
                self.download_stats['pricing_rules'] += len(pricing_data['data'])
            
            # Fetch custom fields
            custom_data = self.make_request(f'/catalog/products/{product["id"]}/custom-fields')
            if custom_data and custom_data.get('data'):
                product['custom_fields'] = custom_data['data']

    def save_final_data(self, products, categories):
        print("Saving all data...")
        
        # Save products
        with open(self.data_dir / 'products_complete.json', 'w') as f:
            json.dump(products, f, indent=2)
        
        # Also update the main products file
        with open(self.data_dir / 'products.json', 'w') as f:
            json.dump(products, f, indent=2)
        
        # Save categories
        with open(self.data_dir / 'categories_complete.json', 'w') as f:
            json.dump(categories, f, indent=2)
        
        # Update main categories file
        with open(self.data_dir / 'categories.json', 'w') as f:
            json.dump(categories, f, indent=2)
        
        # Create organized categories for cannabis products
        cannabis_categories = self.organize_cannabis_categories(categories, products)
        with open(self.data_dir / 'cannabis_categories.json', 'w') as f:
            json.dump(cannabis_categories, f, indent=2)

    def organize_cannabis_categories(self, categories, products):
        """Create organized cannabis product categories"""
        
        # Map category names to cannabis-appropriate categories
        cannabis_cats = []
        
        for category in categories:
            # Determine product count in this category
            products_in_cat = [p for p in products if category['id'] in (p.get('categories') or [])]
            
            if len(products_in_cat) > 0:
                # Categorize based on product names
                cat_type = self.determine_category_type(category['name'], products_in_cat)
                
                enhanced_category = {
                    'id': category['id'],
                    'name': category['name'],
                    'display_name': cat_type['display_name'],
                    'description': cat_type['description'],
                    'image_url': category.get('image_url'),
                    'local_image_path': category.get('local_image_path'),
                    'product_count': len(products_in_cat),
                    'sort_order': category.get('sort_order', 0)
                }
                
                cannabis_cats.append(enhanced_category)
        
        return cannabis_cats

    def determine_category_type(self, cat_name, products):
        """Determine cannabis category type based on products"""
        
        product_names = ' '.join([p['name'].lower() for p in products])
        
        if any(word in product_names for word in ['grinder', 'herb']):
            return {
                'display_name': 'Herb Grinders & Accessories',
                'description': 'Premium grinders and herb preparation tools'
            }
        elif any(word in product_names for word in ['vape', 'pen', 'battery']):
            return {
                'display_name': 'Vape Pens & Batteries', 
                'description': 'Vaporizers, pens, and battery accessories'
            }
        elif any(word in product_names for word in ['rolling', 'paper', 'tray', 'cone']):
            return {
                'display_name': 'Rolling Papers & Trays',
                'description': 'Rolling papers, cones, and accessories'
            }
        elif any(word in product_names for word in ['lighter', 'torch']):
            return {
                'display_name': 'Lighters & Torches',
                'description': 'Quality lighters and flame accessories'
            }
        elif any(word in product_names for word in ['jar', 'stash', 'container']):
            return {
                'display_name': 'Storage & Containers',
                'description': 'Airtight jars and storage solutions'
            }
        elif any(word in product_names for word in ['ashtray', 'ash']):
            return {
                'display_name': 'Ashtrays & Accessories',
                'description': 'Ashtrays and smoking accessories'
            }
        else:
            return {
                'display_name': cat_name,
                'description': f'{cat_name} products and accessories'
            }

if __name__ == "__main__":
    STORE_HASH = 'tqjrceegho'
    ACCESS_TOKEN = 'lmg7prm3b0fxypwwaja27rtlvqejic0'
    CLIENT_ID = 'oy5coebc3asdpdjlbzef8y22nv3s477'
    
    downloader = CompleteDownloader(STORE_HASH, ACCESS_TOKEN, CLIENT_ID)
    downloader.download_complete_products()