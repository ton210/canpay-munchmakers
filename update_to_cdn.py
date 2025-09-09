#!/usr/bin/env python3
"""
Update website to use R2 CDN URLs instead of local images
"""

import json
from pathlib import Path

class CDNUpdater:
    def __init__(self):
        self.cdn_base = "https://pub-0cf6e905891a477fbe1dc1b8360ef92c.r2.dev"
        
    def update_products_to_cdn(self):
        print("UPDATING WEBSITE TO USE R2 CDN")
        print("=" * 50)
        
        # Update products.json
        products_file = Path('website/data/products.json')
        if not products_file.exists():
            print("Products file not found")
            return
        
        with open(products_file, 'r') as f:
            products = json.load(f)
        
        updated_count = 0
        
        for product in products:
            # Update primary_image
            if product.get('primary_image') and product['primary_image'].get('local_path'):
                local_path = product['primary_image']['local_path'].replace('\\', '/')
                cdn_url = f"{self.cdn_base}/{local_path}"
                product['primary_image']['cdn_url'] = cdn_url
                updated_count += 1
            
            # Update all_images
            if product.get('all_images'):
                for image in product['all_images']:
                    if image.get('local_path'):
                        local_path = image['local_path'].replace('\\', '/')
                        cdn_url = f"{self.cdn_base}/{local_path}"
                        image['cdn_url'] = cdn_url
                        updated_count += 1
            
            # Update images array
            if product.get('images'):
                for image in product['images']:
                    if image.get('local_path'):
                        local_path = image['local_path'].replace('\\', '/')
                        cdn_url = f"{self.cdn_base}/{local_path}"
                        image['cdn_url'] = cdn_url
                        updated_count += 1
        
        # Save updated products
        with open(products_file, 'w') as f:
            json.dump(products, f, indent=2)
        
        print(f"Updated {updated_count} image URLs to use R2 CDN")
        
        # Update categories.json
        categories_file = Path('website/data/categories.json')
        if categories_file.exists():
            with open(categories_file, 'r') as f:
                categories = json.load(f)
            
            cat_updated = 0
            for category in categories:
                if category.get('local_image_path'):
                    local_path = category['local_image_path'].replace('\\', '/')
                    cdn_url = f"{self.cdn_base}/{local_path}"
                    category['cdn_url'] = cdn_url
                    cat_updated += 1
            
            with open(categories_file, 'w') as f:
                json.dump(categories, f, indent=2)
            
            print(f"Updated {cat_updated} category image URLs")

    def update_javascript_image_functions(self):
        """Update JavaScript to use CDN URLs"""
        print("\nUpdating JavaScript to prioritize CDN URLs...")
        
        js_files = [
            'website/js/app.js',
            'website/js/product.js',
            'website/js/category.js',
            'website/js/products.js'
        ]
        
        for js_file in js_files:
            if Path(js_file).exists():
                with open(js_file, 'r') as f:
                    content = f.read()
                
                # Update getRealProductImage functions to prioritize CDN
                old_pattern = '''if (product.all_images && product.all_images.length > 0) {
            return product.all_images[0].local_path || product.all_images[0].url_zoom;
        }
        
        if (product.primary_image) {
            return product.primary_image.local_path || product.primary_image.url_zoom;
        }'''
        
                new_pattern = '''if (product.all_images && product.all_images.length > 0) {
            return product.all_images[0].cdn_url || product.all_images[0].local_path || product.all_images[0].url_zoom;
        }
        
        if (product.primary_image) {
            return product.primary_image.cdn_url || product.primary_image.local_path || product.primary_image.url_zoom;
        }'''
        
                if old_pattern in content:
                    content = content.replace(old_pattern, new_pattern)
                    
                    with open(js_file, 'w') as f:
                        f.write(content)
                    print(f"Updated: {js_file}")

if __name__ == "__main__":
    updater = CDNUpdater()
    updater.update_products_to_cdn()
    updater.update_javascript_image_functions()
    print("\nWebsite now ready for R2 CDN deployment!")
    print(f"Images will load from: {updater.cdn_base}")