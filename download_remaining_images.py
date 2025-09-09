#!/usr/bin/env python3
"""
Download images for products 81-137 (continuing after product 80)
"""

import requests
import json
import urllib.request
import time
from pathlib import Path

class RemainingImageDownloader:
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
        (self.images_dir / 'products').mkdir(exist_ok=True, parents=True)

    def make_request(self, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            time.sleep(0.03)
            return response.json()
        except Exception as e:
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
        except Exception as e:
            print(f"Failed to download {url}: {e}")
            return None

    def download_remaining_images(self):
        print("DOWNLOADING REMAINING IMAGES (Products 81-137)")
        print("=" * 60)
        
        # Load products to get IDs for 81-137
        with open('website/data/products.json', 'r') as f:
            products = json.load(f)
        
        # Find products from ID ranges that correspond to 81-137
        products_to_download = products[80:137]  # Products 81-137
        
        print(f"Downloading images for {len(products_to_download)} products")
        print()
        
        for i, product in enumerate(products_to_download):
            product_num = i + 81
            print(f"Product {product_num}/137: {product['name'][:40]}...")
            
            # Download all images for this product
            images_data = self.make_request(f'/catalog/products/{product["id"]}/images')
            if images_data and images_data.get('data'):
                product['all_images'] = []
                for j, img in enumerate(images_data['data']):
                    if img.get('url_zoom'):
                        filename = f"products/prod_{product['id']}_img_{j}.jpg"
                        local_path = self.download_image(img['url_zoom'], filename)
                        if local_path:
                            img['local_path'] = local_path
                            product['all_images'].append(img)
                            print(f"  Downloaded image {j+1}/{len(images_data['data'])}")
                
                # Also download main image
                if product.get('primary_image'):
                    filename = f"products/prod_{product['id']}_main.jpg"
                    local_path = self.download_image(product['primary_image']['url_zoom'], filename)
                    if local_path:
                        product['primary_image']['local_path'] = local_path
        
        # Save updated products with new images
        with open('website/data/products.json', 'w') as f:
            json.dump(products, f, indent=2)
        
        print(f"\nCOMPLETE! Downloaded images for products 81-137")

if __name__ == "__main__":
    downloader = RemainingImageDownloader()
    downloader.download_remaining_images()