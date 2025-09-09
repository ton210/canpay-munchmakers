#!/usr/bin/env python3
"""
Simple HTTP server for CanPay Demo Website
"""

import http.server
import socketserver
import os
import json
from pathlib import Path
import webbrowser
import threading
import time

class CanPayHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="website", **kwargs)
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

def start_server():
    PORT = 8080
    os.chdir(Path(__file__).parent)
    
    print("CanPay Demo Store Server Starting...")
    print("=" * 50)
    
    # Check website files
    website_dir = Path('website')
    if not website_dir.exists():
        print("ERROR: Website directory not found!")
        return
    
    # Check data status
    data_dir = Path('data')
    print("Data Status:")
    
    if (data_dir / 'categories.json').exists():
        with open(data_dir / 'categories.json', 'r') as f:
            categories = json.load(f)
        print(f"  Categories: {len(categories)} loaded")
    
    if (data_dir / 'products.json').exists():
        with open(data_dir / 'products.json', 'r') as f:
            products = json.load(f)
        print(f"  Products: {len(products)} loaded")
    
    print(f"\nStarting server on http://localhost:{PORT}")
    print("Available pages:")
    print(f"  Main Store: http://localhost:{PORT}/index.html")
    print(f"  Products: http://localhost:{PORT}/products.html") 
    print(f"  Dashboard: http://localhost:{PORT}/dashboard.html")
    print(f"  Checkout: http://localhost:{PORT}/checkout.html")
    print("\nPress Ctrl+C to stop")
    print("=" * 50)
    
    def open_browser():
        time.sleep(2)
        webbrowser.open(f'http://localhost:{PORT}')
    
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.start()
    
    try:
        with socketserver.TCPServer(("", PORT), CanPayHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
    except Exception as e:
        print(f"Server error: {e}")

if __name__ == "__main__":
    start_server()