<?php
/*
 * CanPay Integration Configuration
 * 
 * IMPORTANT: 
 * 1. Copy this file to 'canpay-config.php'
 * 2. Fill in your actual CanPay credentials below
 * 3. NEVER commit the actual config file to version control
 */

return [
    // Sandbox Configuration (for testing)
    'sandbox' => [
        'app_key' => 'your_sandbox_app_key_here',
        'api_secret' => 'your_sandbox_api_secret_here',
        'integrator_id' => 'your_sandbox_integrator_id_here',
        'canpay_internal_version' => 'your_sandbox_internal_version_here',
        'api_url' => 'https://sandbox-api.canpaydebit.com/integrator/authorize',
        'widget_url' => 'https://sandbox-remotepay.canpaydebit.com/cp-min.js'
    ],
    
    // Production Configuration (for live payments)
    'production' => [
        'app_key' => 'your_production_app_key_here',
        'api_secret' => 'your_production_api_secret_here',
        'integrator_id' => 'your_production_integrator_id_here',
        'canpay_internal_version' => 'your_production_internal_version_here',
        'api_url' => 'https://api.canpaydebit.com/integrator/authorize',
        'widget_url' => 'https://remotepay.canpaydebit.com/cp-min.js'
    ],
    
    // Current environment ('sandbox' or 'production')
    'environment' => 'sandbox',
    
    // Optional webhook settings
    'webhook' => [
        'url' => 'https://yoursite.com/webhook.php',
        'enabled' => false
    ]
];
?>