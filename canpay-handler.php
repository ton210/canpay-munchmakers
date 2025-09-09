<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    exit(0);
}

// Load CanPay Configuration
if (!file_exists('canpay-config.php')) {
    echo json_encode([
        'success' => false, 
        'error' => 'Configuration file not found. Please copy canpay-config.example.php to canpay-config.php and configure your credentials.'
    ]);
    exit;
}

$CONFIG = require 'canpay-config.php';
$ENV = $CONFIG['environment'];
$CANPAY_CONFIG = $CONFIG[$ENV];

if (!$CANPAY_CONFIG['app_key'] || strpos($CANPAY_CONFIG['app_key'], 'your_') === 0) {
    echo json_encode([
        'success' => false, 
        'error' => 'CanPay credentials not configured. Please update canpay-config.php with your actual credentials.'
    ]);
    exit;
}

function createIntentId($amount, $deliveryFee = 0, $splitFundingMerchantId = null) {
    global $CANPAY_CONFIG;
    
    $postData = [
        'app_key' => $CANPAY_CONFIG['app_key'],
        'api_secret' => $CANPAY_CONFIG['api_secret'],
        'integrator_id' => $CANPAY_CONFIG['integrator_id'],
        'canpay_internal_version' => $CANPAY_CONFIG['canpay_internal_version'],
        'auth_only' => 'false',
        'amount' => strval($amount)
    ];
    
    if ($deliveryFee > 0) {
        $postData['delivery_fee'] = strval($deliveryFee);
    }
    
    if ($splitFundingMerchantId) {
        $postData['split_funding_merchant_id'] = $splitFundingMerchantId;
    }
    
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $CANPAY_CONFIG['api_url']);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($postData));
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Accept: application/json',
        'Content-Type: application/x-www-form-urlencoded',
        'User-Agent: PHP-cURL/7.0'
    ]);
    
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    
    if (curl_errno($ch)) {
        curl_close($ch);
        return ['success' => false, 'error' => 'cURL Error: ' . curl_error($ch)];
    }
    
    curl_close($ch);
    
    if ($httpCode !== 200) {
        return ['success' => false, 'error' => 'HTTP Error: ' . $httpCode, 'response' => $response];
    }
    
    $result = json_decode($response, true);
    
    if ($result && isset($result['code']) && $result['code'] === 200) {
        return [
            'success' => true, 
            'intent_id' => $result['data']['intent_id']
        ];
    } else {
        return [
            'success' => false, 
            'error' => $result['message'] ?? 'Unknown error',
            'response' => $result
        ];
    }
}

function verifySignature($responseData, $signature) {
    global $CANPAY_CONFIG;
    
    $expectedSignature = hash_hmac('sha256', $responseData, $CANPAY_CONFIG['api_secret']);
    
    return hash_equals($expectedSignature, $signature);
}

// Handle different actions
$action = $_POST['action'] ?? $_GET['action'] ?? '';

switch ($action) {
    case 'create_intent':
        $amount = floatval($_POST['amount'] ?? 0);
        $deliveryFee = floatval($_POST['delivery_fee'] ?? 0);
        $splitFundingMerchantId = $_POST['split_funding_merchant_id'] ?? null;
        
        if ($amount <= 0) {
            echo json_encode(['success' => false, 'error' => 'Invalid amount']);
            exit;
        }
        
        $result = createIntentId($amount, $deliveryFee, $splitFundingMerchantId);
        echo json_encode($result);
        break;
        
    case 'verify_payment':
        $responseData = $_POST['response'] ?? '';
        $signature = $_POST['signature'] ?? '';
        
        if (empty($responseData) || empty($signature)) {
            echo json_encode(['success' => false, 'error' => 'Missing response data or signature']);
            exit;
        }
        
        $isValid = verifySignature($responseData, $signature);
        
        if ($isValid) {
            $paymentData = json_decode($responseData, true);
            
            // Here you would typically:
            // 1. Store the transaction details in your database
            // 2. Update order status
            // 3. Send confirmation emails
            // 4. Clear the cart
            
            echo json_encode([
                'success' => true,
                'message' => 'Payment verified successfully',
                'transaction' => $paymentData
            ]);
        } else {
            echo json_encode(['success' => false, 'error' => 'Invalid signature']);
        }
        break;
        
    default:
        echo json_encode(['success' => false, 'error' => 'Invalid action']);
        break;
}
?>