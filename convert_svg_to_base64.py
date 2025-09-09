#!/usr/bin/env python3
"""
Convert SVG logo to base64 data URI to eliminate loading issues
"""

import base64
import os

def convert_svg_to_base64():
    """Convert the SVG logo to base64 data URI"""
    
    svg_path = "website/assets/images/canpay-logo.svg"
    
    if not os.path.exists(svg_path):
        print(f"SVG file not found: {svg_path}")
        return None
    
    # Read SVG file
    with open(svg_path, 'r', encoding='utf-8') as f:
        svg_content = f.read()
    
    # Convert to base64
    svg_bytes = svg_content.encode('utf-8')
    base64_svg = base64.b64encode(svg_bytes).decode('utf-8')
    
    # Create data URI
    data_uri = f"data:image/svg+xml;base64,{base64_svg}"
    
    print("SVG converted to base64 data URI:")
    print("=" * 50)
    print(data_uri[:100] + "..." if len(data_uri) > 100 else data_uri)
    print("=" * 50)
    print(f"Total length: {len(data_uri)} characters")
    
    return data_uri

def update_html_with_base64(data_uri):
    """Update HTML files to use base64 data URI instead of external SVG"""
    
    files_to_update = [
        "website/index.html",
        "website/cart.html",
        "canpay-munchmakers-deploy/index.html",
        "canpay-munchmakers-deploy/cart.html"
    ]
    
    old_src = 'https://pub-0cf6e905891a477fbe1dc1b8360ef92c.r2.dev/images/canpay-logo.svg'
    new_src = data_uri
    
    for file_path in files_to_update:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if old_src in content:
                content = content.replace(old_src, new_src)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"Updated: {file_path}")
            else:
                print(f"No update needed: {file_path}")
        else:
            print(f"File not found: {file_path}")

if __name__ == "__main__":
    print("Converting CanPay logo to base64 data URI...")
    data_uri = convert_svg_to_base64()
    
    if data_uri:
        print("\nUpdating HTML files...")
        update_html_with_base64(data_uri)
        print("\nSVG logo converted to base64 - no more external loading issues!")