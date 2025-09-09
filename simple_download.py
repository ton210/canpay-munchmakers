#!/usr/bin/env python3
"""
Simple BigCommerce Product Downloader - No Emojis
"""

import requests
import json
import os
import urllib.request
import time
from pathlib import Path
import sys

class SimpleDownloader:
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

    def make_request(self, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            time.sleep(0.05)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

    def download_image(self, url, filename):
        if not url:
            return None
        try:
            filepath = self.images_dir / filename
            if filepath.exists():
                return str(filepath)
            urllib.request.urlretrieve(url, filepath)
            return str(filepath)
        except:
            return None

    def fetch_products(self):
        print("Starting product download...")
        
        # Get total count first
        initial = self.make_request('/catalog/products', {'limit': 1})
        if not initial:
            print("Failed to connect to API")
            return []
        
        total = initial.get('meta', {}).get('pagination', {}).get('total', 0)
        print(f"Total products: {total}")
        
        products = []
        page = 1
        downloaded = 0
        
        while True:
            print(f"Page {page}...", end=" ")
            
            data = self.make_request('/catalog/products', {
                'page': page, 
                'limit': 50,
                'include': 'images,primary_image'
            })
            
            if not data or not data.get('data'):
                break
            
            for product in data['data']:
                downloaded += 1
                progress = (downloaded / total) * 100
                print(f"\r{downloaded}/{total} ({progress:.1f}%) - {product['name'][:30]}...", end="")
                
                # Download main image
                if product.get('primary_image') and product['primary_image'].get('url_zoom'):
                    filename = f"products/prod_{product['id']}.jpg"
                    local_path = self.download_image(product['primary_image']['url_zoom'], filename)
                    product['primary_image']['local_path'] = local_path
                
                # Keep essential data only
                products.append({
                    'id': product['id'],
                    'name': product['name'],
                    'description': product['description'],
                    'price': product['price'],
                    'sale_price': product['sale_price'] if product['sale_price'] != 0 else None,
                    'categories': product['categories'],
                    'primary_image': product.get('primary_image'),
                    'is_visible': product['is_visible'],
                    'inventory_level': product.get('inventory_level', 0)
                })
                
                # Save progress every 25 products
                if downloaded % 25 == 0:
                    with open(self.data_dir / 'products.json', 'w') as f:
                        json.dump(products, f, indent=2)
                    print(f"\nSaved {downloaded} products...")
            
            if page >= data.get('meta', {}).get('pagination', {}).get('total_pages', 1):
                break
            page += 1
        
        # Final save
        with open(self.data_dir / 'products.json', 'w') as f:
            json.dump(products, f, indent=2)
        
        print(f"\nCOMPLETE! Downloaded {len(products)} products")
        return products

if __name__ == "__main__":
    STORE_HASH = 'tqjrceegho'
    ACCESS_TOKEN = 'lmg7prm3b0fxypwwaja27rtlvqejic0'
    CLIENT_ID = 'oy5coebc3asdpdjlbzef8y22nv3s477'
    
    downloader = SimpleDownloader(STORE_HASH, ACCESS_TOKEN, CLIENT_ID)
    products = downloader.fetch_products()