# Deploy to canpay.munchmakers.com

## Option 1: GitHub Pages with Custom Domain

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "CanPay store for canpay.munchmakers.com"
   git branch -M main
   git remote add origin https://github.com/USERNAME/REPOSITORY.git
   git push -u origin main
   ```

2. **Configure GitHub Pages:**
   - Go to repository Settings > Pages
   - Source: Deploy from a branch
   - Branch: main / root
   - The CNAME file will automatically set the custom domain

3. **DNS Configuration:**
   Point canpay.munchmakers.com to GitHub Pages:
   ```
   Type: CNAME
   Name: canpay
   Value: USERNAME.github.io
   ```

## Option 2: Cloudflare Pages

1. **Connect Repository:**
   - Go to Cloudflare Pages
   - Connect your GitHub repository
   - Build settings: None (static site)
   - Build output directory: / (root)

2. **Custom Domain:**
   - In Cloudflare Pages, go to Custom domains
   - Add: canpay.munchmakers.com
   - Cloudflare will handle DNS automatically if domain is on Cloudflare

## Option 3: Direct File Upload

1. **Upload to Web Server:**
   - Upload all files in this directory to your web server
   - Point canpay.munchmakers.com to the upload directory

2. **DNS Configuration:**
   ```
   Type: A
   Name: canpay
   Value: YOUR_SERVER_IP
   ```

## Files Ready:
- [+] CNAME file configured
- [+] SEO meta tags added
- [+] All images on R2 CDN
- [+] Mobile-responsive design
- [+] CanPay branding and checkout

Your CanPay store will be live at: https://canpay.munchmakers.com
