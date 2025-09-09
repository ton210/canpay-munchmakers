#!/usr/bin/env python3
"""
Create a completely professional, fancy CanPay demo website
"""

import json
import shutil
from pathlib import Path

def create_professional_site():
    print("CREATING PROFESSIONAL CANPAY DEMO WEBSITE")
    print("=" * 50)
    
    # Create professional website directory
    pro_site = Path('professional_canpay')
    if pro_site.exists():
        shutil.rmtree(pro_site)
    pro_site.mkdir()
    
    # Copy optimized data
    github_dir = Path('github_deploy')
    
    # Create directories
    (pro_site / 'css').mkdir()
    (pro_site / 'js').mkdir()
    (pro_site / 'data').mkdir()
    (pro_site / 'assets').mkdir()
    
    # Copy data files
    if (github_dir / 'data').exists():
        for data_file in (github_dir / 'data').glob('*.json'):
            shutil.copy2(data_file, pro_site / 'data')
    
    print("✅ Professional website structure created")
    print(f"📁 Location: {pro_site.absolute()}")

if __name__ == "__main__":
    create_professional_site()