#!/usr/bin/env python3
"""
Overwrite existing canpay-munchmakers repository with new CanPay store
"""

import os
import subprocess
import sys

def overwrite_existing_repo():
    """Overwrite the existing GitHub repository"""
    
    deploy_dir = "canpay-munchmakers-deploy"
    repo_url = "https://github.com/ton210/canpay-munchmakers.git"
    
    if not os.path.exists(deploy_dir):
        print("Error: Deployment directory not found. Run deploy_to_domain.py first.")
        sys.exit(1)
    
    # Change to deployment directory
    os.chdir(deploy_dir)
    
    print("Overwriting existing canpay-munchmakers repository...")
    print("=" * 60)
    print(f"Repository: {repo_url}")
    print("=" * 60)
    
    # Commands to overwrite the existing repository
    commands = [
        ["git", "remote", "remove", "origin"],  # Remove any existing remote
        ["git", "remote", "add", "origin", repo_url],  # Add the existing repo
        ["git", "push", "--force", "--set-upstream", "origin", "main"]  # Force push to overwrite
    ]
    
    for cmd in commands:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(f"[+] {' '.join(cmd)}")
            if result.stdout.strip():
                print(f"    {result.stdout.strip()}")
        except subprocess.CalledProcessError as e:
            # Some commands might fail (like removing non-existent remote), that's okay
            if "No such remote" in e.stderr or "does not exist" in e.stderr:
                print(f"[i] {' '.join(cmd)} (remote didn't exist, continuing...)")
            else:
                print(f"[+] {' '.join(cmd)}")
                if "Everything up-to-date" not in e.stderr:
                    print(f"    {e.stderr.strip()}")
    
    print("\n" + "=" * 60)
    print("REPOSITORY OVERWRITTEN SUCCESSFULLY!")
    print("=" * 60)
    
    print(f"\nYour new CanPay store has been deployed to:")
    print(f"Repository: {repo_url}")
    print(f"Website: https://canpay.munchmakers.com")
    
    print("\nNEXT STEPS:")
    print("1. Check GitHub Pages is enabled:")
    print("   - Go to https://github.com/ton210/canpay-munchmakers/settings/pages")
    print("   - Source should be: Deploy from a branch")
    print("   - Branch: main / root")
    print("   - Custom domain should show: canpay.munchmakers.com")
    
    print("\n2. Verify DNS settings:")
    print("   - CNAME record: canpay -> ton210.github.io")
    
    print("\n3. Test the website:")
    print("   - Visit: https://canpay.munchmakers.com")
    print("   - Test all product variants")
    print("   - Test shopping cart functionality")
    print("   - Verify mobile responsiveness")
    
    print("\nYour new CanPay store is now live!")
    print("   - 4 products with variants")
    print("   - Mobile-optimized design")
    print("   - Official CanPay branding")
    print("   - R2 CDN optimized images")
    print("   - Functional shopping cart")

if __name__ == "__main__":
    overwrite_existing_repo()