class ShoppingCart {
  constructor() {
    this.items = JSON.parse(localStorage.getItem('cartItems')) || [];
    this.updateCartCount();
    this.bindEvents();
  }

  bindEvents() {
    document.addEventListener('click', (e) => {
      if (e.target.matches('.buy-with-canpay')) {
        e.preventDefault();
        this.buyWithCanPay(e.target);
      } else if (e.target.matches('.quantity-btn')) {
        this.updateQuantity(e.target);
      } else if (e.target.matches('.variant-option')) {
        this.selectVariant(e.target);
      } else if (e.target.matches('.remove-item')) {
        this.removeItem(e.target.dataset.itemId);
      }
    });

    document.addEventListener('change', (e) => {
      if (e.target.matches('.quantity-input')) {
        this.updateCartItemQuantity(e.target);
      }
    });
  }

  buyWithCanPay(button) {
    const productCard = button.closest('.product-card');
    if (!productCard) {
      alert('Error: Product not found. Please try again.');
      return;
    }
    
    const productId = productCard.dataset.productId;
    const title = productCard.querySelector('.product-title').textContent;
    const price = parseFloat(productCard.querySelector('.product-price').textContent.replace('$', ''));
    const image = productCard.querySelector('.product-image').src;
    
    const selectedVariant = productCard.querySelector('.variant-option.selected');
    const variant = selectedVariant ? selectedVariant.textContent : 'Default';
    
    const quantityInput = productCard.querySelector('.quantity-input');
    const quantity = quantityInput ? parseInt(quantityInput.value) : 1;

    const itemId = `${productId}-${variant}`;
    
    // Clear cart and add only this item
    this.items = [{
      id: itemId,
      productId,
      title,
      variant,
      price,
      quantity,
      image
    }];

    this.saveCart();
    this.updateCartCount();
    
    // Go directly to cart/checkout page
    window.location.href = 'cart.html';
  }

  removeItem(itemId) {
    this.items = this.items.filter(item => item.id !== itemId);
    this.saveCart();
    this.updateCartCount();
    this.renderCart();
  }

  updateCartItemQuantity(input) {
    const itemId = input.dataset.itemId;
    const newQuantity = parseInt(input.value);
    
    if (newQuantity <= 0) {
      this.removeItem(itemId);
      return;
    }

    const item = this.items.find(item => item.id === itemId);
    if (item) {
      item.quantity = newQuantity;
      this.saveCart();
      this.updateCartCount();
      this.renderCart();
    }
  }

  selectVariant(variantButton) {
    const productCard = variantButton.closest('.product-card');
    productCard.querySelectorAll('.variant-option').forEach(btn => btn.classList.remove('selected'));
    variantButton.classList.add('selected');
    
    // Update product image if variant has specific image
    const productImage = productCard.querySelector('.product-image');
    const variantImage = variantButton.dataset.image;
    if (variantImage) {
      productImage.src = variantImage;
    }
  }

  updateQuantity(button) {
    const quantityInput = button.parentElement.querySelector('.quantity-input');
    const currentValue = parseInt(quantityInput.value);
    
    if (button.textContent === '+') {
      quantityInput.value = currentValue + 1;
    } else if (button.textContent === '-' && currentValue > 1) {
      quantityInput.value = currentValue - 1;
    }
  }

  updateCartCount() {
    const totalItems = this.items.reduce((sum, item) => sum + item.quantity, 0);
    const cartCountElement = document.querySelector('.cart-count');
    if (cartCountElement) {
      cartCountElement.textContent = totalItems;
      cartCountElement.style.display = totalItems > 0 ? 'flex' : 'none';
    }
  }

  getTotal() {
    return this.items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
  }

  renderCart() {
    const cartContainer = document.querySelector('.cart-items');
    if (!cartContainer) return;

    if (this.items.length === 0) {
      cartContainer.innerHTML = `
        <div class="empty-cart">
          <h3>Your cart is empty</h3>
          <p>Add some products to get started!</p>
          <a href="index.html" class="btn btn-primary">Continue Shopping</a>
        </div>
      `;
      document.querySelector('.cart-summary').style.display = 'none';
      return;
    }

    cartContainer.innerHTML = this.items.map(item => `
      <div class="cart-item">
        <img src="${item.image}" alt="${item.title}" class="cart-item-image">
        <div class="cart-item-info">
          <div class="cart-item-title">${item.title}</div>
          <div class="cart-item-variant">${item.variant}</div>
        </div>
        <div class="quantity-selector">
          <input type="number" value="${item.quantity}" min="1" class="quantity-input" data-item-id="${item.id}">
        </div>
        <div class="cart-item-price">$${(item.price * item.quantity).toFixed(2)}</div>
        <button class="remove-item" data-item-id="${item.id}">×</button>
      </div>
    `).join('');

    document.querySelector('.cart-total .total-amount').textContent = `$${this.getTotal().toFixed(2)}`;
    document.querySelector('.cart-summary').style.display = 'block';
  }

  saveCart() {
    localStorage.setItem('cartItems', JSON.stringify(this.items));
  }

  async checkout() {
    if (this.items.length === 0) {
      alert('Your cart is empty!');
      return;
    }

    const checkoutBtn = document.querySelector('.canpay-checkout');
    const originalText = checkoutBtn.textContent;
    
    try {
      // Disable button and show loading
      checkoutBtn.disabled = true;
      checkoutBtn.textContent = 'Processing...';
      
      const total = this.getTotal();
      
      // For demo purposes, we'll create a mock intent_id
      // In production, this should come from your backend
      const mockIntentId = `intent_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      
      // Launch CanPay widget directly
      await this.launchCanPayWidget(mockIntentId, total);
      
    } catch (error) {
      console.error('CanPay checkout error:', error);
      alert('There was an error processing your payment. Please try again.');
    } finally {
      // Re-enable button
      checkoutBtn.disabled = false;
      checkoutBtn.textContent = originalText;
    }
  }

  async launchCanPayWidget(intentId, amount) {
    return new Promise((resolve, reject) => {
      // Configure CanPay widget
      const config = {
        intent_id: intentId,
        amount: amount.toFixed(2),
        tip_amount: "0.00",
        delivery_fee: "0.00",
        is_guest: "true",
        merchant_order_id: `order-${Date.now()}`,
        passthrough: {
          cart_items: this.items.map(item => ({
            id: item.id,
            title: item.title,
            variant: item.variant,
            quantity: item.quantity,
            price: item.price
          }))
        },
        
        // Callback when payment is processed
        processed_callback: (response) => {
          this.handlePaymentResult(response);
          resolve(response);
        },
        
        // Callback for intent validation errors
        intentId_validation_callback: (response) => {
          console.error('Intent ID validation failed:', response);
          reject(new Error('Payment validation failed'));
        },
        
        // Optional: callback for login failures
        login_callback: (response) => {
          console.log('Login callback:', response);
        },
        
        // Optional: callback for account linking
        link_callback: (response) => {
          console.log('Link callback - auth_id:', response.data.auth_id);
          // Store auth_id for future passwordless payments if needed
        }
      };
      
      // Initialize CanPay widget
      try {
        if (typeof canpay !== 'undefined') {
          canpay.init(config);
        } else {
          reject(new Error('CanPay widget not loaded'));
        }
      } catch (error) {
        reject(error);
      }
    });
  }

  async handlePaymentResult(response) {
    try {
      // For demo purposes, we'll accept the payment response directly
      // In production, you should verify the payment with your backend
      
      console.log('Payment response received:', response);
      
      // Parse the response data
      const paymentData = JSON.parse(response.response);
      
      // Check if payment was successful
      if (paymentData.payment_status === 'processed' || paymentData.status === 'success') {
        this.showPaymentSuccess(paymentData);
        
        // Clear cart after successful payment
        this.items = [];
        this.saveCart();
        this.updateCartCount();
        this.renderCart();
      } else {
        throw new Error('Payment was not processed successfully');
      }
      
    } catch (error) {
      console.error('Payment verification error:', error);
      this.showPaymentError(error.message);
    }
  }

  showPaymentSuccess(paymentData) {
    const cartContainer = document.querySelector('.cart-items');
    cartContainer.innerHTML = `
      <div class="payment-success">
        <div class="success-icon">✅</div>
        <h2>Payment Successful!</h2>
        <p>Transaction ID: ${paymentData.canpay_transaction_number || 'DEMO_' + Date.now()}</p>
        <p>Amount: $${paymentData.amount || this.getTotal().toFixed(2)}</p>
        <p>Time: ${new Date().toLocaleString()}</p>
        <a href="index.html" class="btn btn-primary">Continue Shopping</a>
      </div>
    `;
    document.querySelector('.cart-summary').style.display = 'none';
  }

  showPaymentError(errorMessage) {
    alert(`Payment Error: ${errorMessage}\n\nPlease try again or contact support.`);
  }
}

// Initialize cart when DOM loads
document.addEventListener('DOMContentLoaded', () => {
  window.cart = new ShoppingCart();
  
  // Render cart if on cart page
  if (document.querySelector('.cart-items')) {
    window.cart.renderCart();
  }
  
  // Bind checkout button
  const checkoutBtn = document.querySelector('.canpay-checkout');
  if (checkoutBtn) {
    checkoutBtn.addEventListener('click', () => window.cart.checkout());
  }
});