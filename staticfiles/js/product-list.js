// ===== PRODUCT LISTING FUNCTIONALITY =====

// Filter functionality
function clearFilters() {
    // Reset all checkboxes
    document.querySelectorAll('.filter-checkbox input').forEach(checkbox => {
        checkbox.checked = false;
    });
    
    // Reset price range
    document.getElementById('priceRange').value = 0;
    document.getElementById('minPrice').value = '';
    document.getElementById('maxPrice').value = '';
    
    // Reset sort
    document.getElementById('sortSelect').value = '';
    
    // Reload page or apply filters
    window.location.reload();
}

// Quick view functionality
function quickView(productId) {
    // Show loading in modal
    document.getElementById('quickViewContent').innerHTML = '<div class="text-center"><div class="spinner-border"></div></div>';
    
    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('quickViewModal'));
    modal.show();
    
    // Load product details via AJAX
    fetch(`/product/${productId}/quick-view/`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('quickViewContent').innerHTML = data.html;
        })
        .catch(error => {
            document.getElementById('quickViewContent').innerHTML = '<div class="alert alert-danger">Không thể tải thông tin sản phẩm</div>';
        });
}

// Initialize product listing functionality
document.addEventListener('DOMContentLoaded', function() {
    // Add to cart functionality
    document.querySelectorAll('[data-product-id]').forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-product-id');
            if (this.classList.contains('add-to-cart-btn') || this.classList.contains('btn-primary')) {
                addToCart(productId);
            } else if (this.classList.contains('quick-view-btn')) {
                quickView(productId);
            }
        });
    });

    // View toggle functionality
    document.querySelectorAll('[data-view]').forEach(button => {
        button.addEventListener('click', function() {
            const view = this.dataset.view;
            
            // Update active button
            document.querySelectorAll('[data-view]').forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Update grid class
            const grid = document.getElementById('productsGrid');
            grid.className = `products-grid products-${view}`;
        });
    });

    // Sort functionality
    const sortSelect = document.getElementById('sortSelect');
    if (sortSelect) {
        sortSelect.addEventListener('change', function() {
            const sort = this.value;
            if (sort) {
                const url = new URL(window.location);
                url.searchParams.set('sort', sort);
                window.location = url;
            }
        });
    }

    // Price range functionality
    const priceRange = document.getElementById('priceRange');
    const minPrice = document.getElementById('minPrice');
    const maxPrice = document.getElementById('maxPrice');

    if (priceRange && minPrice && maxPrice) {
        // Update price inputs when range changes
        priceRange.addEventListener('input', function() {
            const value = this.value;
            maxPrice.value = value;
        });

        // Update range when price inputs change
        minPrice.addEventListener('input', function() {
            if (parseInt(this.value) > parseInt(maxPrice.value)) {
                maxPrice.value = this.value;
            }
        });

        maxPrice.addEventListener('input', function() {
            if (parseInt(this.value) < parseInt(minPrice.value)) {
                minPrice.value = this.value;
            }
        });
    }

    // Filter checkbox functionality
    document.querySelectorAll('.filter-checkbox input').forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            // Apply filters when checkbox changes
            applyFilters();
        });
    });
});

// Apply filters function
function applyFilters() {
    const selectedBrands = [];
    const selectedStatus = [];
    
    // Get selected brands
    document.querySelectorAll('.brand-filters input:checked').forEach(checkbox => {
        selectedBrands.push(checkbox.value);
    });
    
    // Get selected status
    document.querySelectorAll('.status-filters input:checked').forEach(checkbox => {
        selectedStatus.push(checkbox.value);
    });
    
    // Get price range
    const minPrice = document.getElementById('minPrice').value;
    const maxPrice = document.getElementById('maxPrice').value;
    
    // Build URL with filters
    const url = new URL(window.location);
    
    if (selectedBrands.length > 0) {
        url.searchParams.set('brand', selectedBrands.join(','));
    } else {
        url.searchParams.delete('brand');
    }
    
    if (selectedStatus.length > 0) {
        url.searchParams.set('status', selectedStatus.join(','));
    } else {
        url.searchParams.delete('status');
    }
    
    if (minPrice) {
        url.searchParams.set('min_price', minPrice);
    } else {
        url.searchParams.delete('min_price');
    }
    
    if (maxPrice) {
        url.searchParams.set('max_price', maxPrice);
    } else {
        url.searchParams.delete('max_price');
    }
    
    // Navigate to filtered URL
    window.location = url;
} 