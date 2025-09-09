#!/usr/bin/env python3
"""
Smart download - only get remaining products 81-137 and upload only NEW images to R2
"""

import requests
import json
import urllib.request
import boto3
import time
from pathlib import Path
from botocore.config import Config

class SmartRemainingDownloader:
    def __init__(self):
        # BigCommerce API
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
        
        # R2 Configuration
        self.r2_client = boto3.client(
            's3',
            endpoint_url='https://0e6d346a9d941a3a45d02b7fe387cdaf.r2.cloudflarestorage.com',
            aws_access_key_id='a450d3d4b5ecf998466e15ba6a884093',
            aws_secret_access_key='7323f180d819d8cf47f8b43c27631543548f0f3b89fc9ac39f9d01994cb72e07',
            config=Config(signature_version='s3v4'),
            region_name='auto'
        )
        self.bucket = 'munchmakers-grinder'
        self.cdn_base = 'https://pub-0cf6e905891a477fbe1dc1b8360ef92c.r2.dev'
        
        # Directories
        self.images_dir = Path('website/images')
        self.data_dir = Path('website/data')
        (self.images_dir / 'products').mkdir(exist_ok=True, parents=True)
        
        self.new_images_uploaded = 0

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

    def upload_to_r2(self, local_path, r2_key):
        """Upload image to R2 if it doesn't exist"""
        try:
            # Check if already exists
            try:
                self.r2_client.head_object(Bucket=self.bucket, Key=r2_key)
                return f"{self.cdn_base}/{r2_key}"  # Already exists
            except:
                pass  # Doesn't exist, continue with upload
            
            # Upload new image
            with open(local_path, 'rb') as f:
                self.r2_client.upload_fileobj(
                    f, self.bucket, r2_key,
                    ExtraArgs={'ContentType': 'image/jpeg', 'CacheControl': 'public, max-age=31536000'}
                )
            
            self.new_images_uploaded += 1
            return f"{self.cdn_base}/{r2_key}"
            
        except Exception as e:
            print(f"R2 upload failed: {e}")
            return None

    def download_and_upload_remaining(self):
        print("SMART DOWNLOAD - PRODUCTS 81-137 ONLY")
        print("=" * 50)
        
        # Load existing products
        with open(self.data_dir / 'products.json', 'r') as f:
            products = json.load(f)
        
        print(f"Total products: {len(products)}")
        
        # Process only products without complete image data
        products_to_process = []
        for product in products:
            # Check if product has complete image data
            if not product.get('all_images') or len(product.get('all_images', [])) == 0:
                products_to_process.append(product)
        
        print(f"Products needing images: {len(products_to_process)}")
        
        for i, product in enumerate(products_to_process):
            product_id = product['id']
            print(f"Product {i+1}/{len(products_to_process)}: {product['name'][:40]}...")
            
            # Get all images for this product
            images_data = self.make_request(f'/catalog/products/{product_id}/images')
            if images_data and images_data.get('data'):
                product['all_images'] = []
                
                for j, img in enumerate(images_data['data']):
                    if img.get('url_zoom'):
                        # Download locally
                        filename = f"products/prod_{product_id}_img_{j}.jpg"
                        local_path = self.download_image(img['url_zoom'], filename)
                        
                        if local_path:
                            # Upload to R2
                            r2_key = f"images/{filename}"
                            cdn_url = self.upload_to_r2(local_path, r2_key)
                            
                            # Update image data
                            img['local_path'] = local_path
                            img['cdn_url'] = cdn_url
                            product['all_images'].append(img)
                
                print(f"  Images: {len(product['all_images'])}, R2 uploads: {self.new_images_uploaded}")
            
            # Update primary image with CDN URL
            if product.get('primary_image'):
                filename = f"products/prod_{product_id}_main.jpg"
                if product['primary_image'].get('url_zoom'):
                    local_path = self.download_image(product['primary_image']['url_zoom'], filename)
                    if local_path:
                        r2_key = f"images/{filename}"
                        cdn_url = self.upload_to_r2(local_path, r2_key)
                        product['primary_image']['local_path'] = local_path
                        product['primary_image']['cdn_url'] = cdn_url
        
        # Save updated products
        with open(self.data_dir / 'products.json', 'w') as f:
            json.dump(products, f, indent=2)
        
        print(f"\nSMART DOWNLOAD COMPLETE!")
        print(f"New images uploaded to R2: {self.new_images_uploaded}")
        print(f"Total products with complete data: {len([p for p in products if p.get('all_images')])}")

if __name__ == "__main__":
    downloader = SmartRemainingDownloader()
    downloader.download_and_upload_remaining()