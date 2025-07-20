function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function updateCartItemsCount(count) {
    const cartItemsCountElement = document.querySelector('.cart-items-count');
    if (cartItemsCountElement) {
        cartItemsCountElement.textContent = count;
    }
}

function addToCart(productId, size) {
    console.log(`Adding to cart - Product ID: ${productId}, Size: ${size}`);  // Debug log
    
    fetch('/add_to_cart/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            product_id: productId,
            size: size
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Add to cart response:', data);  // Debug log
        if (data.success) {
            // Cập nhật số lượng sản phẩm trong giỏ hàng
            updateCartItemsCount(data.cart_items_count);
            alert(`Đã thêm ${data.product_name} vào giỏ hàng`);
        } else {
            alert(data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}