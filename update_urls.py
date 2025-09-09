#!/usr/bin/env python3
"""
Update all local image URLs to use R2 CDN URLs
"""

import os
import re

def update_urls_in_file(file_path, cdn_url):
    """Update URLs in a single file"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace local asset URLs with CDN URLs
    content = re.sub(r'src="assets/images/', f'src="{cdn_url}/images/', content)
    content = re.sub(r'data-image="assets/images/', f'data-image="{cdn_url}/images/', content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated URLs in: {file_path}")

def update_all_urls():
    """Update URLs in all HTML files"""
    
    cdn_url = "https://pub-0cf6e905891a477fbe1dc1b8360ef92c.r2.dev"
    website_dir = "website"
    
    # Find all HTML files
    html_files = []
    for root, dirs, files in os.walk(website_dir):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    # Update each file
    for file_path in html_files:
        update_urls_in_file(file_path, cdn_url)
    
    print(f"\nUpdated {len(html_files)} HTML files with CDN URLs")
    print(f"CDN URL: {cdn_url}")

if __name__ == "__main__":
    update_all_urls()