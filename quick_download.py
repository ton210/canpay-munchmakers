#!/usr/bin/env python3
"""
Optimized BigCommerce Product Downloader with Progress Updates
Focuses on product names, images, and essential data
"""

import requests
import json
import os
import urllib.request
import time
from pathlib import Path
import sys

class QuickProductDownloader:
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
        """Make API request with error handling"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            time.sleep(0.05)  # Faster rate limiting
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching {endpoint}: {e}")
            return None

    def download_image(self, url, filename):
        """Download image efficiently"""
        if not url:
            return None
            
        try:
            filepath = self.images_dir / filename
            if filepath.exists():
                return str(filepath)
                
            urllib.request.urlretrieve(url, filepath)
            return str(filepath)
        except Exception as e:
            return None

    def fetch_products_quick(self):
        """Fetch products with progress updates"""
        print("🚀 Quick Product Download Starting...")
        print("=" * 50)
        
        # First, get total count
        initial_data = self.make_request('/catalog/products', {'limit': 1})
        if not initial_data:
            print("❌ Failed to connect to BigCommerce API")
            return []
        
        total_products = initial_data.get('meta', {}).get('pagination', {}).get('total', 0)
        print(f"📦 Total products to download: {total_products}")
        print()
        
        products = []
        page = 1
        downloaded_count = 0
        
        while True:
            print(f"⬇️  Downloading page {page}...", end=" ")
            sys.stdout.flush()
            
            data = self.make_request('/catalog/products', {
                'page': page, 
                'limit': 50,  # Smaller batches for faster processing
                'include': 'images,primary_image'
            })
            
            if not data or not data.get('data'):
                break
            
            page_products = data['data']
            print(f"Got {len(page_products)} products")
            
            for i, product in enumerate(page_products):
                downloaded_count += 1
                
                # Progress update
                progress = (downloaded_count / total_products) * 100
                print(f"📥 {downloaded_count}/{total_products} ({progress:.1f}%) - {product['name'][:40]}{'...' if len(product['name']) > 40 else ''}")
                
                # Download primary image only
                if product.get('primary_image') and product['primary_image'].get('url_zoom'):
                    filename = f"products/product_{product['id']}_main.jpg"
                    local_path = self.download_image(product['primary_image']['url_zoom'], filename)
                    product['primary_image']['local_path'] = local_path
                
                # Simplified product data
                simplified_product = {
                    'id': product['id'],
                    'name': product['name'],
                    'description': product['description'],
                    'price': product['price'],
                    'sale_price': product['sale_price'] if product['sale_price'] != 0 else None,
                    'sku': product['sku'],
                    'weight': product['weight'],
                    'categories': product['categories'],
                    'primary_image': product.get('primary_image'),
                    'inventory_level': product['inventory_level'],
                    'is_visible': product['is_visible'],
                    'availability': product['availability']
                }
                
                products.append(simplified_product)
                
                # Save progress every 10 products
                if downloaded_count % 10 == 0:
                    with open(self.data_dir / 'products_partial.json', 'w') as f:
                        json.dump(products, f, indent=2)
            
            # Check pagination
            if page >= data.get('meta', {}).get('pagination', {}).get('total_pages', 1):
                break
            page += 1
        
        # Save final products data
        with open(self.data_dir / 'products.json', 'w') as f:
            json.dump(products, f, indent=2)
        
        # Remove partial file
        partial_file = self.data_dir / 'products_partial.json'
        if partial_file.exists():
            partial_file.unlink()
        
        print()
        print("✅ Product download complete!")
        print(f"📦 Downloaded {len(products)} products")
        
        return products

    def create_sample_data_if_needed(self):
        """Create sample data for immediate testing"""
        
        # Check if we have any products data
        products_file = self.data_dir / 'products.json'
        partial_file = self.data_dir / 'products_partial.json'
        
        if not products_file.exists() and not partial_file.exists():
            print("📝 Creating sample product data for immediate testing...")
            
            sample_products = [
                {
                    'id': 1, 'name': 'Organic Trail Mix', 
                    'description': 'Premium organic trail mix with nuts and dried fruits',
                    'price': 12.99, 'sale_price': None, 'categories': [1], 'is_visible': True,
                    'primary_image': {'url_zoom': 'https://via.placeholder.com/400x400/2ECC71/FFFFFF?text=Trail+Mix'}
                },
                {
                    'id': 2, 'name': 'Premium Coffee Beans',
                    'description': 'Single-origin Colombian coffee beans roasted to perfection',
                    'price': 18.95, 'sale_price': 15.95, 'categories': [2], 'is_visible': True,
                    'primary_image': {'url_zoom': 'https://via.placeholder.com/400x400/27AE60/FFFFFF?text=Coffee'}
                },
                {
                    'id': 3, 'name': 'Mediterranean Meal Kit',
                    'description': 'Complete meal kit with fresh ingredients and recipes',
                    'price': 34.99, 'sale_price': None, 'categories': [3], 'is_visible': True,
                    'primary_image': {'url_zoom': 'https://via.placeholder.com/400x400/2ECC71/FFFFFF?text=Meal+Kit'}
                }
            ]
            
            with open(self.data_dir / 'products_sample.json', 'w') as f:
                json.dump(sample_products, f, indent=2)
                
            print("✅ Sample data created - website ready for testing!")

if __name__ == "__main__":
    # MunchMakers store credentials
    STORE_HASH = 'tqjrceegho'
    ACCESS_TOKEN = 'lmg7prm3b0fxypwwaja27rtlvqejic0'
    CLIENT_ID = 'oy5coebc3asdpdjlbzef8y22nv3s477'
    
    print("🎯 CanPay MunchMakers Quick Download")
    print("Focus: Product names and images")
    print()
    
    downloader = QuickProductDownloader(STORE_HASH, ACCESS_TOKEN, CLIENT_ID)
    
    # Create sample data for immediate testing
    downloader.create_sample_data_if_needed()
    
    # Start optimized download
    products = downloader.fetch_products_quick()
    
    print(f"🎉 Download complete! Ready to test website.")