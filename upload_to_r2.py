#!/usr/bin/env python3
"""
Upload all cannabis product images to Cloudflare R2 and update website URLs
"""

import boto3
import os
import json
from pathlib import Path
from botocore.config import Config

class R2ImageUploader:
    def __init__(self):
        # R2 Configuration
        self.account_id = '0e6d346a9d941a3a45d02b7fe387cdaf'
        self.access_key = 'a450d3d4b5ecf998466e15ba6a884093'
        self.secret_key = '7323f180d819d8cf47f8b43c27631543548f0f3b89fc9ac39f9d01994cb72e07'
        self.bucket = 'munchmakers-grinder'
        self.endpoint = 'https://0e6d346a9d941a3a45d02b7fe387cdaf.r2.cloudflarestorage.com'
        self.public_url = 'https://pub-0cf6e905891a477fbe1dc1b8360ef92c.r2.dev'
        
        # Configure boto3 client for R2
        self.s3_client = boto3.client(
            's3',
            endpoint_url=self.endpoint,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            config=Config(signature_version='s3v4'),
            region_name='auto'
        )
        
        self.uploaded_count = 0
        self.url_mapping = {}

    def upload_all_images(self):
        print("UPLOADING CANNABIS PRODUCT IMAGES TO R2 CDN")
        print("=" * 60)
        
        # Find all images
        images_dir = Path('website/images')
        if not images_dir.exists():
            print("Images directory not found!")
            return
        
        # Get all image files
        image_files = list(images_dir.rglob('*.jpg')) + list(images_dir.rglob('*.png'))
        total_images = len(image_files)
        
        print(f"Total images to upload: {total_images}")
        print()
        
        # Upload each image
        for i, image_path in enumerate(image_files):
            self.upload_single_image(image_path, i + 1, total_images)
        
        # Save URL mapping
        self.save_url_mapping()
        
        print("\nR2 UPLOAD COMPLETE!")
        print("=" * 60)
        print(f"Uploaded: {self.uploaded_count} images")
        print(f"CDN Base URL: {self.public_url}")
        
        # Update website files
        self.update_website_urls()

    def upload_single_image(self, image_path, current, total):
        try:
            # Create R2 key (path in bucket)
            relative_path = image_path.relative_to(Path('website'))
            r2_key = str(relative_path).replace('\\', '/')
            
            # Upload to R2
            with open(image_path, 'rb') as file:
                self.s3_client.upload_fileobj(
                    file, 
                    self.bucket, 
                    r2_key,
                    ExtraArgs={
                        'ContentType': 'image/jpeg',
                        'CacheControl': 'public, max-age=31536000'  # 1 year cache
                    }
                )
            
            # Create public URL
            public_url = f"{self.public_url}/{r2_key}"
            
            # Store mapping
            local_path = str(relative_path)
            self.url_mapping[local_path] = public_url
            
            self.uploaded_count += 1
            progress = (current / total) * 100
            
            print(f"{current}/{total} ({progress:.1f}%) - {image_path.name}")
            
        except Exception as e:
            print(f"ERROR uploading {image_path.name}: {e}")

    def save_url_mapping(self):
        """Save URL mapping for website updates"""
        mapping_file = Path('website/data/r2_image_mapping.json')
        with open(mapping_file, 'w') as f:
            json.dump(self.url_mapping, f, indent=2)
        print(f"\nURL mapping saved: {len(self.url_mapping)} images")

    def update_website_urls(self):
        """Update all JSON files to use R2 URLs instead of local paths"""
        print("\nUpdating website to use R2 CDN URLs...")
        
        # Update products.json
        self.update_products_json()
        
        # Update categories.json
        self.update_categories_json()
        
        print("Website URLs updated to use R2 CDN!")

    def update_products_json(self):
        products_file = Path('website/data/products.json')
        if not products_file.exists():
            return
        
        with open(products_file, 'r') as f:
            products = json.load(f)
        
        # Update product image URLs
        for product in products:
            # Update primary_image
            if product.get('primary_image') and product['primary_image'].get('local_path'):
                local_path = product['primary_image']['local_path'].replace('\\', '/')
                if local_path in self.url_mapping:
                    product['primary_image']['r2_url'] = self.url_mapping[local_path]
            
            # Update all_images
            if product.get('all_images'):
                for image in product['all_images']:
                    if image.get('local_path'):
                        local_path = image['local_path'].replace('\\', '/')
                        if local_path in self.url_mapping:
                            image['r2_url'] = self.url_mapping[local_path]
            
            # Update images array
            if product.get('images'):
                for image in product['images']:
                    if image.get('local_path'):
                        local_path = image['local_path'].replace('\\', '/')
                        if local_path in self.url_mapping:
                            image['r2_url'] = self.url_mapping[local_path]
        
        # Save updated products
        with open(products_file, 'w') as f:
            json.dump(products, f, indent=2)

    def update_categories_json(self):
        categories_file = Path('website/data/categories.json')
        if not categories_file.exists():
            return
        
        with open(categories_file, 'r') as f:
            categories = json.load(f)
        
        # Update category image URLs
        for category in categories:
            if category.get('local_image_path'):
                local_path = category['local_image_path'].replace('\\', '/')
                if local_path in self.url_mapping:
                    category['r2_url'] = self.url_mapping[local_path]
        
        # Save updated categories
        with open(categories_file, 'w') as f:
            json.dump(categories, f, indent=2)

if __name__ == "__main__":
    uploader = R2ImageUploader()
    uploader.upload_all_images()