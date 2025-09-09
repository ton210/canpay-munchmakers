#!/usr/bin/env python3
"""
Prepare CanPay website for GitHub Pages deployment
"""

import shutil
import os
from pathlib import Path
import zipfile

def prepare_github_deployment():
    print("PREPARING CANPAY WEBSITE FOR GITHUB PAGES")
    print("=" * 60)
    
    # Create GitHub deployment directory
    github_deploy = Path('github_deploy')
    if github_deploy.exists():
        shutil.rmtree(github_deploy)
    github_deploy.mkdir()
    
    # Copy website files (excluding large images)
    website_dir = Path('website')
    
    # Copy HTML files
    html_files = list(website_dir.glob('*.html'))
    for html_file in html_files:
        if 'old' not in html_file.name:  # Skip backup files
            shutil.copy2(html_file, github_deploy)
            print(f"Copied: {html_file.name}")
    
    # Copy CSS directory
    if (website_dir / 'css').exists():
        shutil.copytree(website_dir / 'css', github_deploy / 'css')
        print("Copied: css/ directory")
    
    # Copy JS directory  
    if (website_dir / 'js').exists():
        shutil.copytree(website_dir / 'js', github_deploy / 'js')
        print("Copied: js/ directory")
    
    # Copy data directory (JSON files only)
    if (website_dir / 'data').exists():
        shutil.copytree(website_dir / 'data', github_deploy / 'data')
        print("Copied: data/ directory")
    
    # Create README.md for GitHub
    readme_content = '''# CanPay Cannabis Demo Store

A comprehensive demo showcasing CanPay payment integration with a real cannabis e-commerce store.

## 🌟 Features

- **Mobile-first responsive design**
- **Real cannabis product data** from MunchMakers
- **CanPay payment integration** with JavaScript SDK
- **Advanced pricing rules** and minimum order quantities
- **Product variants** (up to 50 per product)
- **Bulk pricing display** 
- **Touch-optimized** mobile experience

## 🖼️ Images

Product images are served from Cloudflare R2 CDN for optimal performance:
- **CDN URL**: https://pub-0cf6e905891a477fbe1dc1b8360ef92c.r2.dev
- **Total Images**: 2,100+ cannabis product images
- **Performance**: Global edge caching for fast loading

## 🚀 Live Demo

Visit the live demo at: **canpay.munchmakers.com**

## 📱 Pages

- **Home**: Mobile-optimized homepage with featured products
- **Products**: Complete product catalog with filtering
- **Categories**: Cannabis accessories organized by type
- **Product Details**: Individual product pages with variants
- **Dashboard**: CanPay integration configuration
- **Checkout**: CanPay payment flow demonstration

## 🛠️ Technology Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Images**: Cloudflare R2 CDN
- **Hosting**: GitHub Pages
- **Payment**: CanPay JavaScript SDK
- **Data Source**: BigCommerce API (MunchMakers store)

## 🔧 Local Development

```bash
# Clone repository
git clone [repository-url]

# Serve locally
python -m http.server 8080

# Visit http://localhost:8080
```

## 📊 Data Statistics

- **Products**: 137 cannabis accessories
- **Categories**: 47 organized categories  
- **Product Variants**: Up to 50 per product
- **Pricing Rules**: Up to 20 bulk pricing tiers
- **Images**: 2,100+ high-resolution product photos

## 🏪 Product Categories

- **Grinders**: Herb grinders (2-piece, 4-piece, ceramic)
- **Vape Pens**: Vaporizers and 510 batteries
- **Rolling Papers**: Papers, cones, tips, and accessories
- **Lighters**: BIC lighters and torch accessories
- **Storage**: Stash jars and smell-proof containers
- **Ashtrays**: Ceramic, metal, and portable ashtrays

## 🎯 CanPay Integration

This demo showcases a complete CanPay integration including:

- **Payment buttons** replacing traditional "Add to Cart"
- **Secure checkout** with bank-to-bank transfers
- **Mobile-optimized** payment flow
- **Integration dashboard** with configuration options
- **Real minimum order** quantity handling
- **Bulk pricing** support

## 📄 License

This is a demonstration project showcasing CanPay payment integration.
'''

    with open(github_deploy / 'README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("Created: README.md")
    
    # Create .gitignore
    gitignore_content = '''# Dependencies
node_modules/
npm-debug.log*

# Local development
.DS_Store
Thumbs.db

# IDE files
.vscode/
.idea/
*.swp
*.swo

# Logs
*.log

# Local images (served from R2 CDN)
images/

# Backup files
*_old.*
*_backup.*
'''

    with open(github_deploy / '.gitignore', 'w') as f:
        f.write(gitignore_content)
    
    print("Created: .gitignore")
    
    # Create index.html redirect if needed
    print()
    print("GITHUB DEPLOYMENT READY!")
    print("=" * 60)
    print(f"📁 Location: {github_deploy.absolute()}")
    print("📄 Files ready for GitHub Pages:")
    
    for item in github_deploy.rglob('*'):
        if item.is_file():
            size_mb = item.stat().st_size / (1024 * 1024)
            print(f"   {item.relative_to(github_deploy)} ({size_mb:.2f} MB)")
    
    print()
    print("🚀 NEXT STEPS:")
    print("1. Initialize Git repository:")
    print(f"   cd {github_deploy.absolute()}")
    print("   git init")
    print("   git add .")
    print('   git commit -m "Initial CanPay demo website"')
    print()
    print("2. Create GitHub repository:")
    print("   git remote add origin https://github.com/[username]/canpay-munchmakers")
    print("   git branch -M main") 
    print("   git push -u origin main")
    print()
    print("3. Enable GitHub Pages:")
    print("   Repository Settings → Pages → Source: Deploy from branch")
    print("   Branch: main, Folder: / (root)")
    print()
    print("4. Add custom domain:")
    print("   Pages Settings → Custom domain: canpay.munchmakers.com")

if __name__ == "__main__":
    prepare_github_deployment()