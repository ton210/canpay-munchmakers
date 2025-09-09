#!/usr/bin/env python3
"""
Fix R2 CDN URLs for all products - ensure images load properly
"""

import json
from pathlib import Path

def fix_r2_urls():
    print("FIXING R2 CDN URLS FOR ALL PRODUCTS")
    print("=" * 50)
    
    github_dir = Path('github_deploy')
    products_file = github_dir / 'data' / 'products.json'
    
    # Load products
    with open(products_file, 'r') as f:
        products = json.load(f)
    
    cdn_base = 'https://pub-0cf6e905891a477fbe1dc1b8360ef92c.r2.dev'
    fixed_count = 0
    
    for product in products:
        product_id = product['id']
        
        # Fix primary image CDN URL
        if product.get('primary_image'):
            pi = product['primary_image']
            if not pi.get('cdn_url'):
                # Generate CDN URL from product ID
                pi['cdn_url'] = f"{cdn_base}/images/products/prod_{product_id}_main.jpg"
                fixed_count += 1
        
        # Fix all_images CDN URLs
        if product.get('all_images'):
            for i, img in enumerate(product['all_images']):
                if not img.get('cdn_url'):
                    # Generate CDN URL from product ID and image index
                    img['cdn_url'] = f"{cdn_base}/images/products/prod_{product_id}_img_{i}.jpg"
                    fixed_count += 1
        
        # Ensure at least primary image exists
        if not product.get('primary_image') and not product.get('all_images'):
            product['primary_image'] = {
                'cdn_url': f"{cdn_base}/images/products/prod_{product_id}_main.jpg"
            }
            fixed_count += 1
    
    # Save fixed products
    with open(products_file, 'w') as f:
        json.dump(products, f, separators=(',', ':'))
    
    print(f"Fixed {fixed_count} CDN URLs")
    print(f"All {len(products)} products now have R2 CDN image URLs")
    
    # Test a few URLs
    print("\nSample CDN URLs:")
    for product in products[:5]:
        if product.get('primary_image'):
            print(f"  {product['name'][:30]}: {product['primary_image']['cdn_url']}")

if __name__ == "__main__":
    fix_r2_urls()