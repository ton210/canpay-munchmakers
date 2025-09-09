# CanPay Store

A modern, mobile-optimized e-commerce website featuring CanPay-branded cannabis accessories with integrated CanPay checkout functionality.

## Features

- **4 Premium Products**: Aluminum Ashtrays, Aluminum Grinders, Joint Cases, and Tin Rolling Trays
- **Variant Selection**: Color and size options for each product
- **Shopping Cart**: Fully functional cart with quantity management
- **CanPay Integration**: Secure checkout exclusively through CanPay
- **Mobile Optimized**: Responsive design for all devices
- **Modern Design**: Clean, professional CanPay branding

## Products Included

1. **CanPay Aluminum Ashtray** - $24.99
   - Available in: Black, Blue, Gold, Gray, Green, Purple, Red, Rose Gold, Silver

2. **CanPay Aluminum Grinder** - $39.99
   - Available in: Black, Blue, Gold, Green, Gunmetal Grey, Pink, Purple, Red, Rose Gold

3. **CanPay Joint Case** - $19.99
   - Available in: Black, Blue, Gold, Green, Grey, Red, Rose Gold, Silver

4. **CanPay Tin Rolling Tray** - $14.99
   - Available in: 18" x 14", 27" x 16"

## Project Structure

```
CanPay/
├── website/
│   ├── index.html              # Main store page
│   ├── cart.html               # Shopping cart page
│   └── assets/
│       ├── css/
│       │   └── style.css       # CanPay-branded styles
│       ├── js/
│       │   └── cart.js         # Shopping cart functionality
│       └── images/
│           ├── canpay-logo.svg # CanPay logo
│           └── products/       # Optimized product images
├── optimize_images.py          # Image processing script
├── upload_to_r2_new.py        # R2 upload script (needs credentials)
├── serve_website.py           # Local development server
└── README.md                  # This file
```

## Quick Start

### Local Development

1. **Start the local server:**
   ```bash
   python serve_website.py
   ```

2. **Open your browser:**
   - Visit: http://localhost:8000
   - The website will automatically open in your default browser

### Testing the Website

- Browse products on the main page
- Test variant selection (colors/sizes)
- Add items to cart with different quantities
- View cart functionality
- Test mobile responsiveness

## Deployment

### Option 1: Cloudflare R2 + Pages

1. **Upload assets to R2:**
   - Update credentials in `upload_to_r2_new.py`
   - Run: `python upload_to_r2_new.py`

2. **Deploy to Cloudflare Pages:**
   - Connect your GitHub repository
   - Set build command: (none needed - static site)
   - Set publish directory: `website`

### Option 2: GitHub Pages

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "CanPay store website"
   git push origin main
   ```

2. **Enable GitHub Pages:**
   - Go to repository settings
   - Enable Pages from `/website` directory
   - Your site will be available at: `https://username.github.io/repository-name`

## Customization

### Update Product Information

Edit the product cards in `website/index.html`:
- Change prices in `.product-price`
- Update descriptions in `.product-description`
- Modify variant options in `.variant-options`

### Modify CanPay Integration

Update the checkout function in `website/assets/js/cart.js`:
- Integrate with actual CanPay API
- Configure payment processing
- Set up order confirmation

### Brand Customization

Modify `website/assets/css/style.css`:
- Update CSS custom properties for colors
- Change fonts or layout
- Adjust responsive breakpoints

## Browser Compatibility

- Modern browsers (Chrome, Firefox, Safari, Edge)
- Mobile browsers (iOS Safari, Chrome Mobile)
- Progressive enhancement for older browsers

## Performance Features

- Optimized images (max 800px width, compressed)
- Minimal CSS and JavaScript
- Local storage for cart persistence
- Cached assets with appropriate headers

## Security Features

- Client-side only (no server-side vulnerabilities)
- Local storage for cart (no sensitive data)
- HTTPS ready for production deployment
- CanPay secure checkout integration

## Development Notes

- All images were optimized from the source directory
- Product variants are dynamically handled
- Cart state persists across page refreshes
- Mobile-first responsive design approach

## Next Steps for Production

1. **Configure R2 Credentials**: Update `upload_to_r2_new.py` with actual credentials
2. **CanPay API Integration**: Replace mock checkout with real CanPay API calls  
3. **Domain Setup**: Configure custom domain for professional appearance
4. **Analytics**: Add Google Analytics or similar tracking
5. **SEO**: Add meta descriptions, structured data, sitemap
6. **Performance**: Set up CDN and optimize loading speeds

## Support

For issues or customizations:
- Check browser console for JavaScript errors
- Verify all image paths are correct
- Ensure CanPay integration is properly configured
- Test on various devices and browsers

---

**Powered by CanPay** - Secure cannabis payments made simple.