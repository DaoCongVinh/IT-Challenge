 // Function to add a product to the cart
 function addToCart(productId) {
    const sizeElement = document.querySelector("select");
    let selectedSize = sizeElement ? sizeElement.value : null;

    if (!selectedSize || selectedSize === "Select Size") {
        selectedSize = "M"; // Default size
    }

    // Define the URL for adding a product to the cart
    const url = "/add_to_cart/";

    // Prepare the data payload
    const data = {
        product_id: productId,
        size: selectedSize
    };

    // Make an AJAX POST request
    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken") // Django's CSRF token
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error("Failed to add product to cart");
        }
    })
    .then(data => {
        // Notify the user of success
        alert(`Product ${data.product_name} (Size: ${data.size}) has been added to the cart!`);
        // Update cart count in header immediately
        if (typeof data.cart_items_count !== 'undefined') {
            updateCartCount(data.cart_items_count);
        }
    })
    .catch(error => {
        console.error(error);
        alert("An error occurred while adding the product to the cart.");
    });
}

// Helper function to get CSRF token for Django
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Update cart count in header
function updateCartCount(count) {
    const cartCountEls = document.querySelectorAll('.cart-count');
    cartCountEls.forEach(el => {
        el.textContent = count;
    });
}

document.addEventListener('DOMContentLoaded', function () {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value; // Get CSRF token

    // Lấy số lượng sản phẩm trong giỏ hàng khi load trang
    fetch('/cart/items-count/')
        .then(response => response.json())
        .then(data => {
            if (typeof data.cart_items_count !== 'undefined') {
                updateCartCount(data.cart_items_count);
            }
        });

    // Add event listeners to quantity inputs
    document.querySelectorAll('.quantity-input').forEach(input => {
        input.addEventListener('change', function () {
            const cartId = this.dataset.cartId;
            const productId = this.dataset.productId;
            const itemId = this.dataset.itemId;
            const quantity = parseInt(this.value, 10);

            if (quantity < 1) {
                alert("Quantity must be at least 1.");
                this.value = 1;
                return;
            }

            // Send AJAX request to update the cart item
            fetch('/update-cart-item/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify({
                    cart_id: cartId,
                    product_id: productId,
                    item_id: itemId,
                    quantity: quantity,
                }),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Update total price for the item
                        document.querySelector(`#item-total-${itemId}`).textContent = data.item_total_price + '₫';
                        
                        // Update total cart price and item count
                        document.querySelector('#cart-total').textContent = data.cart_total+'₫';
                        document.querySelector('#cart-discount-amount').textContent = data.discount_amount+'₫';
                        
                        // Update grand total with bold formatting
                        const grandTotalElement = document.querySelector('#cart-grand-total');
                        grandTotalElement.textContent = data.cart_real_total+'₫';
                        grandTotalElement.style.fontWeight = 'bold';
                        // Update cart count in header
                        if (typeof data.cart_items_count !== 'undefined') {
                            updateCartCount(data.cart_items_count);
                        }
                    } else {
                        alert(data.error || 'Failed to update cart.');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred while updating the cart.');
                });
        });
    });
});




