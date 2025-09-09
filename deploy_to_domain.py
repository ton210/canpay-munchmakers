#!/usr/bin/env python3
"""
Deploy CanPay store to canpay.munchmakers.com
"""

import os
import shutil
import json

def deploy_to_domain():
    """Deploy website for canpay.munchmakers.com"""
    
    # Create domain-specific deployment
    domain_deploy = "canpay-munchmakers-deploy"
    if os.path.exists(domain_deploy):
        shutil.rmtree(domain_deploy)
    
    # Copy deployment files
    shutil.copytree("canpay-store-deploy", domain_deploy)
    
    # Create CNAME file for custom domain
    cname_content = "canpay.munchmakers.com"
    with open(os.path.join(domain_deploy, "CNAME"), "w") as f:
        f.write(cname_content)
    
    # Update meta tags for custom domain
    index_file = os.path.join(domain_deploy, "index.html")
    with open(index_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Add domain-specific meta tags
    meta_tags = '''    <meta name="description" content="Premium CanPay cannabis accessories - Aluminum ashtrays, grinders, joint cases, and rolling trays. Secure checkout with CanPay.">
    <meta property="og:title" content="CanPay Store - Premium Cannabis Accessories">
    <meta property="og:description" content="Discover our exclusive collection of high-quality cannabis accessories, available exclusively through CanPay.">
    <meta property="og:url" content="https://canpay.munchmakers.com">
    <meta property="og:type" content="website">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="CanPay Store">
    <meta name="twitter:description" content="Premium cannabis accessories with secure CanPay checkout.">
    <link rel="canonical" href="https://canpay.munchmakers.com">'''
    
    content = content.replace('<title>CanPay Store - Premium Cannabis Accessories</title>', 
                             f'<title>CanPay Store - Premium Cannabis Accessories</title>\n{meta_tags}')
    
    with open(index_file, "w", encoding="utf-8") as f:
        f.write(content)
    
    # Create deployment instructions for the domain
    domain_instructions = f"""# Deploy to canpay.munchmakers.com

## Option 1: GitHub Pages with Custom Domain

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "CanPay store for canpay.munchmakers.com"
   git branch -M main
   git remote add origin https://github.com/USERNAME/REPOSITORY.git
   git push -u origin main
   ```

2. **Configure GitHub Pages:**
   - Go to repository Settings > Pages
   - Source: Deploy from a branch
   - Branch: main / root
   - The CNAME file will automatically set the custom domain

3. **DNS Configuration:**
   Point canpay.munchmakers.com to GitHub Pages:
   ```
   Type: CNAME
   Name: canpay
   Value: USERNAME.github.io
   ```

## Option 2: Cloudflare Pages

1. **Connect Repository:**
   - Go to Cloudflare Pages
   - Connect your GitHub repository
   - Build settings: None (static site)
   - Build output directory: / (root)

2. **Custom Domain:**
   - In Cloudflare Pages, go to Custom domains
   - Add: canpay.munchmakers.com
   - Cloudflare will handle DNS automatically if domain is on Cloudflare

## Option 3: Direct File Upload

1. **Upload to Web Server:**
   - Upload all files in this directory to your web server
   - Point canpay.munchmakers.com to the upload directory

2. **DNS Configuration:**
   ```
   Type: A
   Name: canpay
   Value: YOUR_SERVER_IP
   ```

## Files Ready:
- [+] CNAME file configured
- [+] SEO meta tags added
- [+] All images on R2 CDN
- [+] Mobile-responsive design
- [+] CanPay branding and checkout

Your CanPay store will be live at: https://canpay.munchmakers.com
"""

    with open(os.path.join(domain_deploy, "DOMAIN_DEPLOYMENT.md"), "w") as f:
        f.write(domain_instructions)
    
    # Create GitHub workflow for automatic deployment
    github_dir = os.path.join(domain_deploy, ".github", "workflows")
    os.makedirs(github_dir, exist_ok=True)
    
    github_workflow = """name: Deploy CanPay Store

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./
        cname: canpay.munchmakers.com
"""
    
    with open(os.path.join(github_dir, "deploy.yml"), "w") as f:
        f.write(github_workflow)
    
    print(f"""
DOMAIN DEPLOYMENT READY!
========================

Created: {domain_deploy}/
Domain: canpay.munchmakers.com

Files configured:
[+] CNAME file created
[+] SEO meta tags added  
[+] GitHub Actions workflow
[+] Domain-specific deployment instructions

Next steps:
1. Upload to GitHub repository
2. Configure DNS settings
3. Enable GitHub Pages or Cloudflare Pages
4. Your CanPay store will be live at https://canpay.munchmakers.com

See {domain_deploy}/DOMAIN_DEPLOYMENT.md for detailed instructions.
""")

if __name__ == "__main__":
    deploy_to_domain()