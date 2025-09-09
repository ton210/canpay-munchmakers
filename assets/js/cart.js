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

  checkout() {
    if (this.items.length === 0) {
      alert('Your cart is empty!');
      return;
    }

    // Redirect to CanPay checkout
    const total = this.getTotal();
    const items = this.items.map(item => ({
      name: `${item.title} - ${item.variant}`,
      quantity: item.quantity,
      price: item.price
    }));

    // This would integrate with actual CanPay API
    console.log('Processing CanPay checkout:', { total, items });
    alert(`Redirecting to CanPay checkout for $${total.toFixed(2)}`);
    
    // Clear cart after successful checkout
    this.items = [];
    this.saveCart();
    this.updateCartCount();
    this.renderCart();
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