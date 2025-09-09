#!/usr/bin/env python3
"""
Fix GitHub Pages data loading by embedding data directly in JavaScript
"""

import json
import os
from pathlib import Path

def embed_data_in_js():
    print("FIXING GITHUB PAGES DATA LOADING")
    print("=" * 50)
    
    github_dir = Path('github_deploy')
    
    # Load data files
    products_file = github_dir / 'data' / 'products.json'
    categories_file = github_dir / 'data' / 'categories.json'
    pricing_file = github_dir / 'data' / 'enhanced_pricing.json'
    
    products = []
    categories = []
    pricing = []
    
    if products_file.exists():
        with open(products_file, 'r') as f:
            products = json.load(f)
        print(f"Loaded {len(products)} products")
    
    if categories_file.exists():
        with open(categories_file, 'r') as f:
            categories = json.load(f)
        print(f"Loaded {len(categories)} categories")
    
    if pricing_file.exists():
        with open(pricing_file, 'r') as f:
            pricing = json.load(f)
        print(f"Loaded {len(pricing)} pricing records")
    
    # Create embedded data JavaScript
    embedded_js = f'''// Embedded Data for GitHub Pages
// Generated automatically to avoid CORS issues

window.CANPAY_DATA = {{
    products: {json.dumps(products, indent=2)},
    categories: {json.dumps(categories, indent=2)},
    enhancedPricing: {json.dumps(pricing, indent=2)},
    timestamp: '{os.path.basename(__file__)} generated this data',
    totalProducts: {len(products)},
    totalCategories: {len(categories)},
    cdnBase: 'https://pub-0cf6e905891a477fbe1dc1b8360ef92c.r2.dev'
}};

console.log('CanPay Data Loaded:', {{
    products: window.CANPAY_DATA.products.length,
    categories: window.CANPAY_DATA.categories.length,
    pricing: window.CANPAY_DATA.enhancedPricing.length
}});
'''
    
    # Save embedded data
    data_js_file = github_dir / 'js' / 'data.js'
    with open(data_js_file, 'w', encoding='utf-8') as f:
        f.write(embedded_js)
    
    print(f"Created: {data_js_file}")
    print(f"Size: {len(embedded_js) / 1024:.1f} KB")
    
    # Update index.html to include data.js
    index_file = github_dir / 'index.html'
    if index_file.exists():
        with open(index_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Add data.js before other scripts
        if '<script src="js/app.js"></script>' in html_content:
            html_content = html_content.replace(
                '<script src="js/app.js"></script>',
                '<script src="js/data.js"></script>\n    <script src="js/app.js"></script>'
            )
            
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print("Updated index.html to include data.js")
    
    print("\nGitHub Pages data loading fix complete!")

if __name__ == "__main__":
    embed_data_in_js()