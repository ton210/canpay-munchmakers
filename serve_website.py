#!/usr/bin/env python3
"""
Simple HTTP server for testing the CanPay website locally
Run: python serve_website.py
Then open: http://localhost:8000
"""

import http.server
import socketserver
import os
import webbrowser
import sys

def serve_website():
    """Start local development server"""
    
    # Change to website directory
    website_dir = os.path.join(os.getcwd(), 'website')
    
    if not os.path.exists(website_dir):
        print("Error: website directory not found!")
        sys.exit(1)
    
    os.chdir(website_dir)
    
    PORT = 8000
    
    class HTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            # Add CORS headers for local development
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            super().end_headers()
    
    with socketserver.TCPServer(("", PORT), HTTPRequestHandler) as httpd:
        print(f"CanPay Store Development Server")
        print(f"==============================")
        print(f"Server running at: http://localhost:{PORT}")
        print(f"Website directory: {website_dir}")
        print(f"Press Ctrl+C to stop the server")
        print()
        
        # Try to open browser automatically
        try:
            webbrowser.open(f'http://localhost:{PORT}')
            print("Opening browser...")
        except:
            print("Please open http://localhost:8000 in your browser")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

if __name__ == "__main__":
    serve_website()