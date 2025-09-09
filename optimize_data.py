#!/usr/bin/env python3
"""
Optimize data for GitHub Pages - remove unnecessary fields to reduce size
"""

import json
from pathlib import Path

def optimize_products_data():
    print("OPTIMIZING DATA FOR GITHUB PAGES")
    print("=" * 40)
    
    github_dir = Path('github_deploy')
    products_file = github_dir / 'data' / 'products.json'
    
    # Load products
    with open(products_file, 'r') as f:
        products = json.load(f)
    
    print(f"Original products: {len(products)}")
    
    # Create optimized products
    optimized_products = []
    
    for product in products:
        # Keep only essential fields
        optimized = {
            'id': product['id'],
            'name': product['name'],
            'price': product['price'],
            'sale_price': product.get('sale_price'),
            'categories': product.get('categories', []),
            'is_visible': product.get('is_visible', True),
            'inventory_level': product.get('inventory_level', 0)
        }
        
        # Add simplified description (clean HTML)
        description = product.get('description', '')
        if description:
            # Remove HTML tags and clean up
            import re
            clean_desc = re.sub(r'<[^>]+>', '', description)
            clean_desc = re.sub(r'&[^;]+;', ' ', clean_desc)
            clean_desc = ' '.join(clean_desc.split())
            
            # Truncate if too long
            if len(clean_desc) > 200:
                clean_desc = clean_desc[:200] + '...'
            
            optimized['description'] = clean_desc
        
        # Add primary image with CDN URL
        if product.get('primary_image'):
            pi = product['primary_image']
            optimized['primary_image'] = {
                'cdn_url': pi.get('cdn_url'),
                'url_zoom': pi.get('url_zoom'),
                'local_path': pi.get('local_path')
            }
        
        # Add first few images only
        if product.get('all_images'):
            optimized['all_images'] = []
            for img in product['all_images'][:6]:  # Only first 6 images
                optimized['all_images'].append({
                    'cdn_url': img.get('cdn_url'),
                    'url_zoom': img.get('url_zoom'),
                    'local_path': img.get('local_path')
                })
        
        # Add simplified variants (only essential info)
        if product.get('variants'):
            optimized['variants'] = []
            for variant in product['variants'][:10]:  # Max 10 variants
                optimized['variants'].append({
                    'id': variant['id'],
                    'price': variant.get('price'),
                    'option_values': variant.get('option_values', [])[:3]  # Max 3 options
                })
        
        # Add simplified pricing rules
        if product.get('pricing_rules'):
            optimized['pricing_rules'] = []
            for rule in product['pricing_rules'][:5]:  # Max 5 pricing rules
                optimized['pricing_rules'].append({
                    'quantity_min': rule['quantity_min'],
                    'quantity_max': rule.get('quantity_max'),
                    'amount': rule['amount']
                })
        
        optimized_products.append(optimized)
    
    # Save optimized data
    optimized_file = github_dir / 'data' / 'products_optimized.json'
    with open(optimized_file, 'w') as f:
        json.dump(optimized_products, f, separators=(',', ':'))  # Compact JSON
    
    # Check sizes
    original_size = products_file.stat().st_size / 1024 / 1024
    optimized_size = optimized_file.stat().st_size / 1024 / 1024
    
    print(f"Original: {original_size:.1f} MB")
    print(f"Optimized: {optimized_size:.1f} MB")
    print(f"Reduction: {((original_size - optimized_size) / original_size * 100):.1f}%")
    
    # Replace original with optimized
    with open(products_file, 'w') as f:
        json.dump(optimized_products, f, separators=(',', ':'))
    
    print("Products data optimized for GitHub Pages!")

if __name__ == "__main__":
    optimize_products_data()