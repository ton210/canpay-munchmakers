#!/usr/bin/env python3
"""
Setup GitHub repository for canpay.munchmakers.com deployment
"""

import os
import subprocess
import sys

def setup_github_repo():
    """Create GitHub repository and deploy"""
    
    deploy_dir = "canpay-munchmakers-deploy"
    
    if not os.path.exists(deploy_dir):
        print("Error: Deployment directory not found. Run deploy_to_domain.py first.")
        sys.exit(1)
    
    # Change to deployment directory
    os.chdir(deploy_dir)
    
    print("Setting up GitHub repository for canpay.munchmakers.com...")
    print("=" * 50)
    
    # Initialize git repository
    commands = [
        ["git", "init"],
        ["git", "add", "."],
        ["git", "commit", "-m", "Initial commit: CanPay store for canpay.munchmakers.com"],
        ["git", "branch", "-M", "main"]
    ]
    
    for cmd in commands:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(f"[+] {' '.join(cmd)}")
            if result.stdout.strip():
                print(f"    {result.stdout.strip()}")
        except subprocess.CalledProcessError as e:
            print(f"[-] {' '.join(cmd)} failed:")
            print(f"  {e.stderr.strip()}")
            if "already exists" not in e.stderr:
                sys.exit(1)
    
    print("\n" + "=" * 50)
    print("NEXT STEPS:")
    print("=" * 50)
    print("\n1. CREATE GITHUB REPOSITORY:")
    print("   - Go to https://github.com/new")
    print("   - Repository name: canpay-store")
    print("   - Make it public")
    print("   - Don't initialize with README (we already have files)")
    print("   - Click 'Create repository'")
    
    print("\n2. CONNECT AND PUSH:")
    print("   - Copy the repository URL from GitHub")
    print("   - Run these commands in this directory:")
    print("   git remote add origin https://github.com/USERNAME/canpay-store.git")
    print("   git push -u origin main")
    
    print("\n3. ENABLE GITHUB PAGES:")
    print("   - Go to repository Settings > Pages")
    print("   - Source: Deploy from a branch")
    print("   - Branch: main / root")
    print("   - GitHub will automatically use the CNAME file")
    
    print("\n4. CONFIGURE DNS:")
    print("   - In your DNS provider (Cloudflare, etc.):")
    print("   - Add CNAME record:")
    print("     Name: canpay")
    print("     Target: USERNAME.github.io")
    
    print("\n5. SSL CERTIFICATE:")
    print("   - GitHub Pages will automatically provision SSL")
    print("   - Your site will be accessible at https://canpay.munchmakers.com")
    
    print("\n" + "=" * 50)
    print("ALTERNATIVE: CLOUDFLARE PAGES")
    print("=" * 50)
    print("1. Push to GitHub first (steps 1-2 above)")
    print("2. Go to Cloudflare Pages")
    print("3. Connect your GitHub repository")
    print("4. Deploy settings:")
    print("   - Framework preset: None")
    print("   - Build command: (leave empty)")
    print("   - Build output directory: /")
    print("5. Add custom domain: canpay.munchmakers.com")
    
    print(f"\nRepository ready in: {os.getcwd()}")
    print("Website will be live at: https://canpay.munchmakers.com")

if __name__ == "__main__":
    setup_github_repo()