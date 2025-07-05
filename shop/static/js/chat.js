// Hàm để hiển thị tin nhắn trong hộp chat
function appendMessage(content, sender = 'bot') {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('chat-message', sender);

    const messageContent = document.createElement('div');
    messageContent.classList.add('message', sender);
    messageContent.innerHTML = content;  // Dùng innerHTML thay vì textContent

    messageDiv.appendChild(messageContent);
    document.getElementById('chat-messages').appendChild(messageDiv);
    document.getElementById('chat-messages').scrollTop = document.getElementById('chat-messages').scrollHeight;
}

// Hàm xử lý khi bấm nút gửi
function sendMessage(event) {
    event.preventDefault(); // Ngừng hành vi mặc định của button (nếu có)

    const input = document.getElementById('chat-input');
    const userMessage = input.value.trim();

    // Kiểm tra nếu input rỗng
    if (userMessage === '') return;

    appendMessage(userMessage, 'user'); // Hiển thị tin nhắn người dùng
    input.value = ''; // Xóa input sau khi gửi

    // Phân tách chiều cao và cân nặng từ input
    const inputParts = userMessage.split(',');

    // Kiểm tra định dạng nhập vào (phải có 2 phần cho size)
    if (inputParts.length === 2) {
        // Gửi yêu cầu đến backend (Django) để nhận size
        const height = inputParts[0].trim();
        const weight = inputParts[1].trim();

        // Kiểm tra nếu chiều cao và cân nặng là số hợp lệ
        if (isNaN(height) || isNaN(weight)) {
            appendMessage("Chiều cao và cân nặng phải là số.", 'bot');
            return;
        }

        fetch('/size-chatbot/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({height: height, weight: weight}), // Gửi dữ liệu
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    appendMessage(data.message, 'bot');
                } else {
                    appendMessage('Xin lỗi, tôi không thể xử lý yêu cầu.', 'bot');
                }
            })
            .catch(() => {
                appendMessage('Đã xảy ra lỗi khi gửi yêu cầu.', 'bot');
            });
    } else {
        // Kiểm tra nếu người dùng yêu cầu sản phẩm
        const productCategory = userMessage.toLowerCase().trim();

        const validCategories = ["cheap", "expensive", "hot", "new", "sales", "clothing"];
        if (validCategories.includes(productCategory)) {
            // Gửi yêu cầu đến backend để lấy sản phẩm
            fetch('/get-products/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({category: productCategory}),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Sử dụng map để tạo ra danh sách sản phẩm với từng sản phẩm xuống dòng
                        let productMessages = data.products.map(product => {
                            return `<div class="product-item"><strong>${product.name}</strong> - ${product.price} VND</div>`;
                        }).join('<br>'); // Dùng <br> để xuống dòng giữa các sản phẩm

                        // Thêm vào hộp chat
                        appendMessage(`Sản phẩm ${productCategory}:\n\n${productMessages}`, 'bot');
                    } else {
                        appendMessage('Không tìm thấy sản phẩm cho danh mục này.', 'bot');
                    }
                })
                .catch(() => {
                    appendMessage('Đã xảy ra lỗi khi lấy sản phẩm.', 'bot');
                });
        } else {
            appendMessage('Vui lòng chọn một danh mục hợp lệ: cheap, expensive, hot, new, sales, clothing.', 'bot');
        }
    }
}

// Bật/tắt khung chat
function toggleChat() {
    const chatContainer = document.querySelector('.chat-container');
    chatContainer.classList.toggle('active');
}
