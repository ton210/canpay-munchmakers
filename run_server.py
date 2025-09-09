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

class CanPayHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="website", **kwargs)
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def start_server():
    PORT = 8080
    
    # Change to the project directory
    os.chdir(Path(__file__).parent)
    
    print("=" * 50)
    print("🚀 CanPay Demo Store Server Starting...")
    print("=" * 50)
    print()
    
    # Check if data is ready
    data_dir = Path('data')
    website_dir = Path('website')
    
    if not website_dir.exists():
        print("❌ Website directory not found!")
        return
    
    print("📂 Website Structure:")
    html_files = list(website_dir.glob('*.html'))
    css_files = list((website_dir / 'css').glob('*.css')) if (website_dir / 'css').exists() else []
    js_files = list((website_dir / 'js').glob('*.js')) if (website_dir / 'js').exists() else []
    
    print(f"   HTML Pages: {len(html_files)}")
    print(f"   CSS Files: {len(css_files)}")  
    print(f"   JS Files: {len(js_files)}")
    print()
    
    print("📊 Data Status:")
    if data_dir.exists():
        try:
            if (data_dir / 'categories.json').exists():
                with open(data_dir / 'categories.json', 'r') as f:
                    categories = json.load(f)
                print(f"   ✅ Categories: {len(categories)} loaded")
            else:
                print("   ⏳ Categories: Not downloaded yet")
                
            if (data_dir / 'products.json').exists():
                with open(data_dir / 'products.json', 'r') as f:
                    products = json.load(f)
                print(f"   ✅ Products: {len(products)} loaded")
            else:
                print("   ⏳ Products: Still downloading...")
        except Exception as e:
            print(f"   ⚠️  Data files exist but may be incomplete")
    else:
        print("   ⏳ Download in progress...")
    
    print()
    print("🌐 Starting local server...")
    
    try:
        with socketserver.TCPServer(("", PORT), CanPayHTTPRequestHandler) as httpd:
            print(f"✅ Server started successfully!")
            print(f"🔗 Local URL: http://localhost:{PORT}")
            print(f"🔗 Network URL: http://127.0.0.1:{PORT}")
            print()
            print("📄 Available Pages:")
            for html_file in html_files:
                print(f"   • http://localhost:{PORT}/{html_file.name}")
            print()
            print("🎯 Main Demo: http://localhost:{PORT}/index.html")
            print("⚙️  Dashboard: http://localhost:{PORT}/dashboard.html")
            print()
            print("🛑 Press Ctrl+C to stop the server")
            print("=" * 50)
            
            # Auto-open browser
            def open_browser():
                time.sleep(2)
                webbrowser.open(f'http://localhost:{PORT}')
            
            browser_thread = threading.Thread(target=open_browser)
            browser_thread.start()
            
            # Start server
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    start_server()