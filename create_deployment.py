#!/usr/bin/env python3
"""
Create deployment package for CanPay demo website
"""

import os
import zipfile
import shutil
from pathlib import Path
import json

def create_deployment_package():
    print("Creating CanPay Demo Website Deployment Package")
    print("=" * 60)
    
    # Paths
    website_dir = Path('website')
    deploy_dir = Path('deployment')
    
    # Create deployment directory
    deploy_dir.mkdir(exist_ok=True)
    
    # Clean up website directory
    print("1. Cleaning up website files...")
    
    # Remove old backup files
    for old_file in website_dir.glob('*_old.*'):
        old_file.unlink()
        print(f"   Removed: {old_file.name}")
    
    # Check website structure
    print("2. Checking website structure...")
    
    html_files = list(website_dir.glob('*.html'))
    css_files = list((website_dir / 'css').glob('*.css')) if (website_dir / 'css').exists() else []
    js_files = list((website_dir / 'js').glob('*.js')) if (website_dir / 'js').exists() else []
    data_files = list((website_dir / 'data').glob('*.json')) if (website_dir / 'data').exists() else []
    
    print(f"   HTML files: {len(html_files)}")
    print(f"   CSS files: {len(css_files)}")
    print(f"   JS files: {len(js_files)}")
    print(f"   Data files: {len(data_files)}")
    
    # Count images
    if (website_dir / 'images').exists():
        image_count = len(list((website_dir / 'images').rglob('*.jpg')))
        print(f"   Images: {image_count}")
    else:
        image_count = 0
        print("   Images: 0 (not found)")
    
    # Create ZIP package
    print("3. Creating deployment ZIP...")
    
    zip_path = deploy_dir / 'canpay_demo_website.zip'
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(website_dir):
            for file in files:
                file_path = Path(root) / file
                archive_path = file_path.relative_to(website_dir)
                zipf.write(file_path, archive_path)
    
    # Get package size
    package_size = zip_path.stat().st_size / (1024 * 1024)  # MB
    
    # Create deployment info
    deployment_info = {
        'package_name': 'CanPay Cannabis Demo Website',
        'version': '1.0.0',
        'created_date': '2024-01-15',
        'total_products': 137,
        'total_categories': 47,
        'total_images': image_count,
        'package_size_mb': round(package_size, 2),
        'recommended_hosting': 'Netlify (Free)',
        'target_domain': 'canpay.munchmakers.com',
        'features': [
            'Mobile-first responsive design',
            'CanPay payment integration',
            'Real cannabis product data',
            'Minimum order quantity display',
            'Bulk pricing rules',
            'Touch-optimized navigation',
            'Integration dashboard'
        ]
    }
    
    with open(deploy_dir / 'deployment_info.json', 'w') as f:
        json.dump(deployment_info, f, indent=2)
    
    # Create README for deployment
    readme_content = f"""# CanPay Demo Website - Ready for Deployment

## Package Contents
- **HTML Pages**: {len(html_files)}
- **CSS Files**: {len(css_files)}
- **JavaScript Files**: {len(js_files)}
- **Product Images**: {image_count}
- **Total Package Size**: {package_size:.1f} MB

## Quick Deploy Steps

### 1. Netlify (FREE - 5 minutes)
1. Go to https://app.netlify.com
2. Upload: canpay_demo_website.zip
3. Add domain: canpay.munchmakers.com
4. Update DNS: CNAME canpay → [netlify-url]

### 2. Vercel (FREE - 5 minutes)  
1. Go to https://vercel.com
2. Import project from ZIP
3. Add domain: canpay.munchmakers.com

### 3. GitHub Pages (FREE - 10 minutes)
1. Create GitHub repo
2. Upload website files
3. Enable Pages
4. Add custom domain

## DNS Setup
```
Type: CNAME
Name: canpay
Value: [hosting-provider-url]
TTL: 3600
```

## Features Included
✅ Mobile-first design
✅ Real cannabis product images ({image_count})
✅ CanPay payment integration
✅ Minimum order quantities
✅ Bulk pricing display
✅ Touch-optimized UI
✅ Integration dashboard
"""

    with open(deploy_dir / 'README.md', 'w') as f:
        f.write(readme_content)
    
    print("4. Deployment package created!")
    print("=" * 60)
    print(f"📦 Package: {zip_path}")
    print(f"📄 Size: {package_size:.1f} MB")
    print(f"🖼️ Images: {image_count}")
    print(f"📁 Ready for upload to canpay.munchmakers.com")
    
    return zip_path, deployment_info

if __name__ == "__main__":
    create_deployment_package()