# 🚀 CanPay Cannabis Demo - GitHub Deployment Instructions

## ✅ Ready for Deployment!

Your CanPay cannabis demo website is 100% ready with:
- **137 cannabis products** from MunchMakers
- **2,100+ images** on R2 CDN
- **Mobile-first** responsive design
- **Real bulk pricing** and minimum order quantities
- **CanPay payment integration**

## 📁 Files Ready in: `github_deploy/`

**Repository**: `canpay-munchmakers`
**Target URL**: `canpay.munchmakers.com`
**GitHub User**: `ton210`

## 🔧 Step-by-Step Deployment:

### 1. Create GitHub Repository
1. Go to https://github.com/ton210
2. Click "New Repository"
3. Name: `canpay-munchmakers`
4. Description: `CanPay cannabis demo with MunchMakers products`
5. Set to **Public**
6. **DO NOT** initialize with README (we already have files)
7. Click "Create Repository"

### 2. Push Code to GitHub
```bash
cd "C:\Users\billi\Documents\Plugins\CanPay\github_deploy"

# Push to GitHub
git push -u origin main
```

### 3. Enable GitHub Pages
1. Go to repository Settings
2. Scroll to "Pages" section  
3. Source: **Deploy from a branch**
4. Branch: **main**
5. Folder: **/ (root)**
6. Click **Save**

### 4. Add Custom Domain
1. In Pages settings, add custom domain: `canpay.munchmakers.com`
2. Click **Save**
3. Wait for DNS check

### 5. Update DNS (in your domain registrar)
Add this CNAME record:
```
Type: CNAME
Name: canpay
Value: ton210.github.io
TTL: 3600
```

## 🌐 Final URLs:
- **GitHub Pages**: https://ton210.github.io/canpay-munchmakers
- **Custom Domain**: https://canpay.munchmakers.com
- **Images CDN**: https://pub-0cf6e905891a477fbe1dc1b8360ef92c.r2.dev

## 📊 What's Included:

### Website Files:
- `index.html` - Mobile-optimized homepage
- `products.html` - Product catalog with filtering
- `category.html` - Category pages
- `product.html` - Individual product details
- `checkout.html` - CanPay checkout flow
- `dashboard.html` - Integration dashboard
- `about.html` - About page

### Data Files:
- `data/products.json` - 137 cannabis products with variants & pricing
- `data/categories.json` - 47 organized categories
- `data/enhanced_pricing.json` - Extracted minimum orders & bulk pricing
- `data/r2_image_mapping.json` - CDN URL mappings

### Styling:
- `css/styles.css` - Mobile-first responsive CSS
- `css/dashboard.css` - Dashboard-specific styles

### JavaScript:
- `js/app.js` - Main application logic
- `js/products.js` - Product catalog functionality  
- `js/category.js` - Category page logic
- `js/product.js` - Product detail functionality
- `js/checkout.js` - Checkout process
- `js/dashboard.js` - Integration dashboard

## 🎯 Features:
✅ Mobile-first responsive design
✅ Real cannabis product data (137 products)
✅ R2 CDN images (2,100+ photos)
✅ CanPay payment integration
✅ Bulk pricing display (up to 20 tiers)
✅ Product variants (up to 50 per product)
✅ Minimum order quantities
✅ Touch-optimized navigation
✅ Integration dashboard

**Ready for production deployment to canpay.munchmakers.com!**