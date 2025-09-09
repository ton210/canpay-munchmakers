#!/usr/bin/env python3
"""
Quick download - skip product 80 and continue from 81+
"""

import requests
import json
import time
from pathlib import Path

class SkipDownloader:
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

    def get_variants_and_pricing(self):
        print("FETCHING REMAINING PRODUCT DATA (Skip to Product 81+)")
        print("=" * 60)
        
        # Load existing products
        with open('website/data/products.json', 'r') as f:
            products = json.load(f)
        
        print(f"Starting with {len(products)} products")
        
        # Process each product for variants and pricing
        for i, product in enumerate(products):
            print(f"Product {i+1}/{len(products)}: {product['name'][:40]}...", end=" ")
            
            # Get variants
            variants_data = self.make_request(f'/catalog/products/{product["id"]}/variants')
            if variants_data and variants_data.get('data'):
                product['variants'] = variants_data['data']
                print(f"Variants: {len(variants_data['data'])}", end=" ")
            
            # Get pricing rules
            pricing_data = self.make_request(f'/catalog/products/{product["id"]}/bulk-pricing-rules')
            if pricing_data and pricing_data.get('data'):
                product['pricing_rules'] = pricing_data['data']
                print(f"Pricing: {len(pricing_data['data'])}", end=" ")
            
            # Get custom fields
            custom_data = self.make_request(f'/catalog/products/{product["id"]}/custom-fields')
            if custom_data and custom_data.get('data'):
                product['custom_fields'] = custom_data['data']
                print(f"Fields: {len(custom_data['data'])}")
            else:
                print("✓")
        
        # Save enhanced products
        with open('website/data/products_enhanced.json', 'w') as f:
            json.dump(products, f, indent=2)
        
        # Also update main file
        with open('website/data/products.json', 'w') as f:
            json.dump(products, f, indent=2)
        
        print(f"\nCOMPLETE! Enhanced {len(products)} products with variants and pricing")

if __name__ == "__main__":
    downloader = SkipDownloader()
    downloader.get_variants_and_pricing()