#!/usr/bin/env python3
"""
Simple final download without emoji characters
"""

import requests
import json
import urllib.request
import time
from pathlib import Path

class SimpleFinalDownloader:
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
        (self.images_dir / 'products').mkdir(exist_ok=True, parents=True)

    def make_request(self, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            time.sleep(0.02)
            return response.json()
        except Exception as e:
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

    def download_missing_images(self):
        print("DOWNLOADING MISSING PRODUCT IMAGES")
        print("=" * 50)
        
        # Load existing products
        with open(self.data_dir / 'products.json', 'r') as f:
            products = json.load(f)
        
        print(f"Processing {len(products)} products for missing images...")
        
        for i, product in enumerate(products):
            product_id = product['id']
            print(f"Product {i+1}/{len(products)}: {product['name'][:40]}...")
            
            # Download primary image if missing
            if product.get('primary_image'):
                filename = f"products/prod_{product_id}_main.jpg"
                if not (self.images_dir / filename).exists():
                    if product['primary_image'].get('url_zoom'):
                        local_path = self.download_image(product['primary_image']['url_zoom'], filename)
                        if local_path:
                            product['primary_image']['local_path'] = local_path
                            print(f"  Downloaded main image")
            
            # Download all product images
            images_data = self.make_request(f'/catalog/products/{product_id}/images')
            if images_data and images_data.get('data'):
                if not product.get('all_images'):
                    product['all_images'] = []
                
                for j, img in enumerate(images_data['data']):
                    filename = f"products/prod_{product_id}_img_{j}.jpg"
                    if not (self.images_dir / filename).exists():
                        if img.get('url_zoom'):
                            local_path = self.download_image(img['url_zoom'], filename)
                            if local_path:
                                img['local_path'] = local_path
                                if img not in product['all_images']:
                                    product['all_images'].append(img)
                
                print(f"  All images: {len(product.get('all_images', []))}")
        
        # Save updated products
        with open(self.data_dir / 'products.json', 'w') as f:
            json.dump(products, f, indent=2)
        
        print("MISSING IMAGES DOWNLOAD COMPLETE!")

if __name__ == "__main__":
    downloader = SimpleFinalDownloader()
    downloader.download_missing_images()