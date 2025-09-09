# CanPay Demo Website Deployment Guide

## Quick Deploy to canpay.munchmakers.com

### Option 1: Netlify (FREE - Recommended)

**Step 1: Prepare Website**
1. Zip the entire `website` folder
2. Go to https://app.netlify.com
3. Drag & drop the zip file
4. Your site goes live instantly!

**Step 2: Add Custom Domain**
1. In Netlify dashboard → Site settings → Domain management
2. Add custom domain: `canpay.munchmakers.com` 
3. Netlify provides DNS instructions

**Step 3: DNS Setup (in your domain provider)**
Add these DNS records:
```
Type: CNAME
Name: canpay
Value: [your-netlify-site].netlify.app
```

### Option 2: Vercel (FREE)

**Step 1: Deploy**
1. Go to https://vercel.com
2. Import your `website` folder
3. Deploy instantly

**Step 2: Custom Domain**
1. Project settings → Domains
2. Add `canpay.munchmakers.com`
3. Follow DNS instructions

### Option 3: GitHub Pages (FREE)

**Step 1: Create Repository**
1. Create GitHub repo: `canpay-demo`
2. Upload `website` folder contents
3. Enable Pages in repo settings

**Step 2: Custom Domain**
1. Settings → Pages → Custom domain
2. Add `canpay.munchmakers.com`
3. Add DNS CNAME record

### Option 4: Shared Hosting ($3-5/month)

**Providers:**
- NameCheap: $2.88/month
- Hostinger: $2.99/month  
- Bluehost: $3.95/month

**Steps:**
1. Purchase hosting
2. Upload website folder via FTP/cPanel
3. Point subdomain to hosting folder

## DNS Configuration

**For munchmakers.com domain:**
```
Type: CNAME
Name: canpay
Value: [hosting-provider-url]
TTL: 3600
```

## Files to Upload

Your website package includes:
- 📁 `website/` folder (complete site)
- 🖼️ 1,931+ product images
- 📦 137 cannabis products
- 📂 47 organized categories
- 💳 Full CanPay integration
- 📱 Mobile-optimized design

## Performance Notes

- **Total size**: ~200MB (with all images)
- **Load time**: <2 seconds (optimized)
- **Mobile-first**: Responsive design
- **Images**: Lazy loading ready

## Security Notes

- No server-side code required
- Static HTML/CSS/JS only
- Safe for any hosting provider
- CanPay integration via JavaScript SDK