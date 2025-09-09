#!/usr/bin/env python3
"""
Extract real pricing rules and minimum quantities from BigCommerce data
"""

import json
import re
from pathlib import Path

def extract_pricing_from_description(description):
    """Extract minimum order quantities and pricing from product descriptions"""
    if not description:
        return None
    
    pricing_info = {}
    
    # Extract minimum order quantities
    min_order_patterns = [
        r'minimum order of (\d+)',
        r'minimum (\d+)',
        r'min order (\d+)',
        r'starting at (\d+) units',
        r'order (\d+)\+',
    ]
    
    for pattern in min_order_patterns:
        match = re.search(pattern, description, re.IGNORECASE)
        if match:
            pricing_info['minimum_order'] = int(match.group(1))
            break
    
    # Extract bulk pricing
    bulk_patterns = [
        r'\$(\d+\.?\d*)\s*each',
        r'starting at \$(\d+\.?\d*)',
        r'wholesale pricing.*\$(\d+\.?\d*)',
        r'bulk pricing.*\$(\d+\.?\d*)',
    ]
    
    for pattern in bulk_patterns:
        match = re.search(pattern, description, re.IGNORECASE)
        if match:
            pricing_info['bulk_start_price'] = float(match.group(1))
            break
    
    return pricing_info if pricing_info else None

def analyze_products():
    products_file = Path('website/data/products.json')
    if not products_file.exists():
        print("Products file not found")
        return
    
    with open(products_file, 'r') as f:
        products = json.load(f)
    
    print("REAL MUNCHMAKERS PRICING ANALYSIS")
    print("=" * 50)
    
    products_with_pricing = []
    
    for product in products:
        # Extract pricing from description
        pricing_info = extract_pricing_from_description(product.get('description', ''))
        
        if pricing_info:
            product_info = {
                'id': product['id'],
                'name': product['name'],
                'price': product['price'],
                'sale_price': product.get('sale_price'),
                'minimum_order': pricing_info.get('minimum_order'),
                'bulk_start_price': pricing_info.get('bulk_start_price'),
                'has_variants': bool(product.get('variants')),
                'has_pricing_rules': bool(product.get('pricing_rules'))
            }
            
            products_with_pricing.append(product_info)
            
            print(f"\nProduct: {product['name'][:40]}...")
            print(f"  Regular Price: ${product['price']}")
            if product.get('sale_price'):
                print(f"  Sale Price: ${product['sale_price']}")
            if pricing_info.get('minimum_order'):
                print(f"  Minimum Order: {pricing_info['minimum_order']} units")
            if pricing_info.get('bulk_start_price'):
                print(f"  Bulk Price: ${pricing_info['bulk_start_price']} each")
    
    print(f"\nSUMMARY:")
    print(f"Total products: {len(products)}")
    print(f"Products with minimum orders: {len([p for p in products_with_pricing if p.get('minimum_order')])}")
    print(f"Products with bulk pricing: {len([p for p in products_with_pricing if p.get('bulk_start_price')])}")
    
    # Save enhanced pricing data
    with open('website/data/enhanced_pricing.json', 'w') as f:
        json.dump(products_with_pricing, f, indent=2)
    
    print(f"\nEnhanced pricing data saved to: enhanced_pricing.json")

if __name__ == "__main__":
    analyze_products()