#!/usr/bin/env python3
"""
Final Complete Download - Get ALL missing products and images
"""

import requests
import json
import urllib.request
import time
from pathlib import Path
import sys

class FinalCompleteDownloader:
    def __init__(self):
        self.store_hash = 'tqjrceegho'
        self.access_token = 'lmg7prm3b0fxypwwaja27rtlvqejic0'
        self.client_id = 'oy5coebc3asdpdjlbzef8y22nv3s477'
        self.base_url = f"https://api.bigcommerce.com/stores/{self.store_hash}/v3"
        self.headers = {
            'X-Auth-Token': self.access_token,
            'X-Auth-Client': self.client_id,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        self.images_dir = Path('website/images')
        self.data_dir = Path('website/data')
        
        # Ensure directories exist
        (self.images_dir / 'products').mkdir(exist_ok=True, parents=True)
        self.data_dir.mkdir(exist_ok=True, parents=True)
        
        self.stats = {
            'products_processed': 0,
            'images_downloaded': 0,
            'variants_found': 0,
            'pricing_rules_found': 0
        }

    def make_request(self, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            time.sleep(0.03)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API Error: {e}")
            return None

    def download_image(self, url, filename):
        if not url:
            return None
        try:
            filepath = self.images_dir / filename
            if filepath.exists():
                return str(filepath)
            
            # Download image
            urllib.request.urlretrieve(url, filepath)
            self.stats['images_downloaded'] += 1
            return str(filepath)
        except Exception as e:
            print(f"Image download failed: {e}")
            return None

    def analyze_current_status(self):
        print("ANALYZING CURRENT STATUS")
        print("=" * 40)
        
        # Check existing products
        products_file = self.data_dir / 'products.json'
        if products_file.exists():
            with open(products_file, 'r') as f:
                products = json.load(f)
            print(f"Current products: {len(products)}")
            
            # Check which products have images
            products_with_images = 0
            products_missing_images = []
            
            for product in products:
                has_image = False
                
                # Check primary image
                if product.get('primary_image') and product['primary_image'].get('local_path'):
                    image_path = self.images_dir / product['primary_image']['local_path'].replace('\\', '/')
                    if image_path.exists():
                        has_image = True
                
                # Check all_images
                if product.get('all_images'):
                    for img in product['all_images']:
                        if img.get('local_path'):
                            image_path = self.images_dir / img['local_path'].replace('\\', '/')
                            if image_path.exists():
                                has_image = True
                                break
                
                if has_image:
                    products_with_images += 1
                else:
                    products_missing_images.append(product['id'])
            
            print(f"Products with images: {products_with_images}")
            print(f"Products missing images: {len(products_missing_images)}")
            
            if products_missing_images:
                print(f"Missing images for products: {products_missing_images[:10]}{'...' if len(products_missing_images) > 10 else ''}")
            
            return products
        else:
            print("No products file found - starting fresh")
            return []

    def complete_all_missing_data(self):
        print("STARTING FINAL COMPLETE DOWNLOAD")
        print("=" * 50)
        
        # Analyze current status
        existing_products = self.analyze_current_status()
        
        # Get fresh product list from API
        print("\nFetching complete product list from BigCommerce...")
        all_products = []
        page = 1
        
        while True:
            print(f"Fetching page {page}...", end=" ")
            data = self.make_request('/catalog/products', {
                'page': page,
                'limit': 250,
                'include': 'images,variants,custom_fields,bulk_pricing_rules,primary_image'
            })
            
            if not data or not data.get('data'):
                break
            
            page_products = data['data']
            print(f"{len(page_products)} products")
            
            for product in page_products:
                # Process each product completely
                self.process_complete_product(product)
                all_products.append(product)
                self.stats['products_processed'] += 1
            
            if page >= data.get('meta', {}).get('pagination', {}).get('total_pages', 1):
                break
            page += 1
        
        # Save complete product data
        with open(self.data_dir / 'products_complete_final.json', 'w') as f:
            json.dump(all_products, f, indent=2)
        
        # Also update main products file
        with open(self.data_dir / 'products.json', 'w') as f:
            json.dump(all_products, f, indent=2)
        
        print(f"\nFINAL DOWNLOAD COMPLETE!")
        print(f"Products processed: {self.stats['products_processed']}")
        print(f"Images downloaded: {self.stats['images_downloaded']}")
        print(f"Variants found: {self.stats['variants_found']}")
        print(f"Pricing rules found: {self.stats['pricing_rules_found']}")
        
        return all_products

    def process_complete_product(self, product):
        """Process a single product completely - images, variants, pricing, etc."""
        product_id = product['id']
        
        print(f"Processing Product {product_id}: {product['name'][:30]}...", end=" ")
        
        # Download primary image
        if product.get('primary_image') and product['primary_image'].get('url_zoom'):
            filename = f"products/prod_{product_id}_main.jpg"
            local_path = self.download_image(product['primary_image']['url_zoom'], filename)
            if local_path:
                product['primary_image']['local_path'] = local_path
        
        # Get and download ALL images for this product
        images_data = self.make_request(f'/catalog/products/{product_id}/images')
        if images_data and images_data.get('data'):
            product['all_images'] = []
            for i, img in enumerate(images_data['data']):
                if img.get('url_zoom'):
                    filename = f"products/prod_{product_id}_img_{i}.jpg"
                    local_path = self.download_image(img['url_zoom'], filename)
                    if local_path:
                        img['local_path'] = local_path
                        product['all_images'].append(img)
            print(f"Images: {len(product['all_images'])}", end=" ")
        
        # Get variants
        variants_data = self.make_request(f'/catalog/products/{product_id}/variants')
        if variants_data and variants_data.get('data'):
            product['variants'] = variants_data['data']
            self.stats['variants_found'] += len(variants_data['data'])
            print(f"Variants: {len(variants_data['data'])}", end=" ")
        
        # Get bulk pricing rules
        pricing_data = self.make_request(f'/catalog/products/{product_id}/bulk-pricing-rules')
        if pricing_data and pricing_data.get('data'):
            product['pricing_rules'] = pricing_data['data']
            self.stats['pricing_rules_found'] += len(pricing_data['data'])
            print(f"Pricing: {len(pricing_data['data'])}", end=" ")
        
        # Get custom fields
        custom_data = self.make_request(f'/catalog/products/{product_id}/custom-fields')
        if custom_data and custom_data.get('data'):
            product['custom_fields'] = custom_data['data']
        
        print("✓")

if __name__ == "__main__":
    downloader = FinalCompleteDownloader()
    products = downloader.complete_all_missing_data()