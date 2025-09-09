#!/usr/bin/env python3
"""
BigCommerce Store Data Fetcher for CanPay Integration
Fetches products, categories, images, pricing rules from MunchMakers store
"""

import requests
import json
import os
import urllib.request
import time
from urllib.parse import urlparse
from pathlib import Path

class BigCommerceAPI:
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

    def make_request(self, endpoint, params=None):
        """Make API request with rate limiting"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            # Rate limiting - BigCommerce allows 450 requests per 30 seconds
            time.sleep(0.1)  # Small delay between requests
            
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {endpoint}: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return None

    def download_image(self, url, filename):
        """Download image from URL"""
        if not url:
            return None
            
        try:
            # Create full path
            filepath = self.images_dir / filename
            
            # Skip if already exists
            if filepath.exists():
                return str(filepath)
                
            # Download image
            urllib.request.urlretrieve(url, filepath)
            print(f"Downloaded: {filename}")
            return str(filepath)
        except Exception as e:
            print(f"Failed to download {url}: {e}")
            return None

    def fetch_categories(self):
        """Fetch all categories"""
        print("Fetching categories...")
        categories = []
        page = 1
        
        while True:
            data = self.make_request('/catalog/categories', {'page': page, 'limit': 250})
            if not data or not data.get('data'):
                break
                
            for category in data['data']:
                # Download category image if available
                image_path = None
                if category.get('image_url'):
                    filename = f"categories/category_{category['id']}.jpg"
                    image_path = self.download_image(category['image_url'], filename)
                
                category['local_image_path'] = image_path
                categories.append(category)
            
            # Check if there are more pages
            if page >= data.get('meta', {}).get('pagination', {}).get('total_pages', 1):
                break
            page += 1
        
        # Save categories data
        with open(self.data_dir / 'categories.json', 'w') as f:
            json.dump(categories, f, indent=2)
        
        print(f"Fetched {len(categories)} categories")
        return categories

    def fetch_products(self):
        """Fetch all products with variants and images"""
        print("Fetching products...")
        products = []
        page = 1
        
        while True:
            data = self.make_request('/catalog/products', {
                'page': page, 
                'limit': 250,
                'include': 'images,variants,custom_fields,bulk_pricing_rules,primary_image'
            })
            
            if not data or not data.get('data'):
                break
            
            for product in data['data']:
                print(f"Processing product: {product['name']}")
                
                # Fetch product images
                product_images = self.fetch_product_images(product['id'])
                product['images'] = product_images
                
                # Fetch product variants
                variants = self.fetch_product_variants(product['id'])
                product['variants'] = variants
                
                # Fetch pricing rules (bulk pricing)
                pricing_rules = self.fetch_product_pricing_rules(product['id'])
                product['pricing_rules'] = pricing_rules
                
                # Fetch custom fields
                custom_fields = self.fetch_product_custom_fields(product['id'])
                product['custom_fields'] = custom_fields
                
                products.append(product)
            
            # Check pagination
            if page >= data.get('meta', {}).get('pagination', {}).get('total_pages', 1):
                break
            page += 1
        
        # Save products data
        with open(self.data_dir / 'products.json', 'w') as f:
            json.dump(products, f, indent=2)
        
        print(f"Fetched {len(products)} products")
        return products

    def fetch_product_images(self, product_id):
        """Fetch images for a specific product"""
        data = self.make_request(f'/catalog/products/{product_id}/images')
        if not data or not data.get('data'):
            return []
        
        images = []
        for img in data['data']:
            # Download image
            filename = f"products/product_{product_id}_image_{img['id']}.jpg"
            local_path = self.download_image(img['url_zoom'], filename)
            
            img['local_path'] = local_path
            images.append(img)
        
        return images

    def fetch_product_variants(self, product_id):
        """Fetch variants for a specific product"""
        data = self.make_request(f'/catalog/products/{product_id}/variants')
        if not data or not data.get('data'):
            return []
        
        variants = []
        for variant in data['data']:
            # Fetch variant image if available
            if variant.get('image_url'):
                filename = f"products/variant_{variant['id']}.jpg"
                local_path = self.download_image(variant['image_url'], filename)
                variant['local_image_path'] = local_path
            
            variants.append(variant)
        
        return variants

    def fetch_product_pricing_rules(self, product_id):
        """Fetch bulk pricing rules for a specific product"""
        data = self.make_request(f'/catalog/products/{product_id}/bulk-pricing-rules')
        if not data or not data.get('data'):
            return []
        
        return data['data']

    def fetch_product_custom_fields(self, product_id):
        """Fetch custom fields for a specific product"""
        data = self.make_request(f'/catalog/products/{product_id}/custom-fields')
        if not data or not data.get('data'):
            return []
        
        return data['data']

    def fetch_store_info(self):
        """Fetch store information"""
        print("Fetching store information...")
        data = self.make_request('/store')
        if data:
            with open(self.data_dir / 'store_info.json', 'w') as f:
                json.dump(data, f, indent=2)
        return data

    def fetch_all_data(self):
        """Fetch all store data"""
        print("Starting data fetch from BigCommerce...")
        
        # Fetch all data
        store_info = self.fetch_store_info()
        categories = self.fetch_categories()
        products = self.fetch_products()
        
        # Create summary
        summary = {
            'store_info': store_info,
            'total_categories': len(categories),
            'total_products': len(products),
            'fetch_date': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        with open(self.data_dir / 'summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\nData fetch complete!")
        print(f"Categories: {len(categories)}")
        print(f"Products: {len(products)}")
        print(f"Data saved in: {self.data_dir}")
        print(f"Images saved in: {self.images_dir}")


if __name__ == "__main__":
    # MunchMakers store credentials
    STORE_HASH = 'tqjrceegho'
    ACCESS_TOKEN = 'lmg7prm3b0fxypwwaja27rtlvqejic0'
    CLIENT_ID = 'oy5coebc3asdpdjlbzef8y22nv3s477'
    
    # Initialize API client
    api = BigCommerceAPI(STORE_HASH, ACCESS_TOKEN, CLIENT_ID)
    
    # Fetch all data
    api.fetch_all_data()