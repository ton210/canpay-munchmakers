# CanPay Store - Cannabis Accessories E-Commerce

A professional e-commerce website for cannabis accessories with integrated CanPay RemotePay payment processing.

## Features

- **Premium Product Catalog**: Aluminum ashtrays, grinders, joint cases, and rolling trays
- **CanPay Integration**: Secure cannabis-compliant payment processing
- **Responsive Design**: Optimized for desktop and mobile devices
- **Shopping Cart**: Add products with variants and quantities
- **Secure Checkout**: HMAC signature verification and payment validation

## CanPay Integration Features

- **RemotePay JavaScript Widget**: Seamless payment experience
- **Intent-based Payments**: Secure payment intent creation
- **HMAC Verification**: Payment signature validation for security
- **Sandbox Support**: Test payments in development environment
- **Error Handling**: Comprehensive error handling and user feedback

## Setup Instructions

### Prerequisites

- PHP 7.4 or higher with cURL extension
- Web server (Apache/Nginx) or local development environment
- CanPay merchant account and API credentials

### 1. CanPay Account Setup

1. Contact CanPay to set up your merchant account
2. Obtain the following credentials:
   - App Key
   - API Secret  
   - Integrator ID
   - CanPay Internal Version
   - Sandbox and Production URLs

### 2. Configuration

1. Copy the configuration template:
   ```bash
   cp canpay-config.example.php canpay-config.php
   ```

2. Edit `canpay-config.php` and add your CanPay credentials:
   ```php
   return [
       'sandbox' => [
           'app_key' => 'your_actual_sandbox_app_key',
           'api_secret' => 'your_actual_sandbox_api_secret',
           'integrator_id' => 'your_actual_sandbox_integrator_id',
           'canpay_internal_version' => 'your_actual_internal_version',
           // ... other config
       ]
   ];
   ```

3. Set the environment to 'sandbox' for testing or 'production' for live payments.

### 3. File Structure

```
website/
├── index.html              # Homepage with product catalog
├── cart.html              # Shopping cart and checkout page
├── canpay-handler.php     # Backend API handler for CanPay integration
├── canpay-config.php      # Configuration file (create from example)
├── canpay-config.example.php # Configuration template
├── README.md              # This file
└── assets/
    ├── css/
    │   └── style.css      # Stylesheet
    └── js/
        └── cart.js        # Shopping cart and payment logic
```

### 4. Security Considerations

- **Never commit** `canpay-config.php` to version control
- Store API secrets securely and restrict file access
- Use HTTPS in production for all transactions
- Validate all payment signatures using HMAC verification

## How It Works

### Payment Flow

1. **Product Selection**: User selects products and variants
2. **Cart Management**: Items added to shopping cart
3. **Checkout Initiation**: User clicks "Pay with CanPay"
4. **Intent Creation**: Backend creates payment intent with CanPay API
5. **Widget Launch**: CanPay payment widget opens for user authentication
6. **Payment Processing**: User completes payment through CanPay
7. **Signature Verification**: Backend verifies payment authenticity
8. **Order Completion**: Success page shown, cart cleared

### Technical Implementation

- **Frontend**: JavaScript handles cart management and CanPay widget initialization
- **Backend**: PHP handles API calls and payment verification
- **Security**: HMAC-SHA256 signatures verify payment authenticity
- **Error Handling**: Comprehensive error handling at all levels

## Testing

### Sandbox Testing

1. Set environment to 'sandbox' in configuration
2. Use sandbox credentials from CanPay
3. Test with CanPay's sandbox payment methods
4. Verify payment flows and error handling

### Production Deployment

1. Update configuration with production credentials
2. Set environment to 'production'
3. Test thoroughly in staging environment
4. Deploy to production server with HTTPS

## File Descriptions

### Core Files

- **`canpay-handler.php`**: Main backend handler for CanPay API integration
- **`cart.js`**: Frontend JavaScript for shopping cart and payment processing
- **`canpay-config.php`**: Configuration file with CanPay credentials (created from example)

### Frontend Files

- **`index.html`**: Homepage with product catalog
- **`cart.html`**: Shopping cart and checkout page
- **`style.css`**: CSS styles for the website

## API Endpoints

### POST /canpay-handler.php

**Create Payment Intent**
```
action=create_intent
amount=25.99
delivery_fee=5.00 (optional)
```

**Verify Payment**
```
action=verify_payment
response=<CanPay response JSON>
signature=<HMAC signature>
```

## Support

For CanPay integration support:
- CanPay Developer Documentation
- CanPay Merchant Support

For technical issues with this implementation:
- Check error logs in browser console and server logs
- Verify configuration file settings
- Ensure all credentials are properly configured

## License

This implementation is provided as an example. Please ensure compliance with all applicable laws and CanPay's terms of service.

---

**Important**: This is a cannabis-related payment processing implementation. Ensure compliance with all local, state, and federal regulations regarding cannabis commerce in your jurisdiction.