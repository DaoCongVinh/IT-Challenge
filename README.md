# IT-Challenge - Hệ thống E-commerce BaRoiBeo

## Thông tin sinh viên
- **Họ và tên:** ĐÀO CÔNG VINH
- **MSSV:** 22130325
- **Dự án:** Hệ thống E-commerce với AI Chatbot và Hệ thống Gợi ý Sản phẩm

## Tổng quan dự án

BaRoiBeo là một hệ thống thương mại điện tử hoàn chỉnh được phát triển bằng Django Framework, tích hợp các công nghệ AI hiện đại để cung cấp trải nghiệm mua sắm thông minh cho người dùng.

## 🚀 Tính năng chính

### 1. Hệ thống Authentication
- ✅ Đăng ký tài khoản mới với validation đầy đủ
- ✅ Đăng nhập/đăng xuất an toàn
- ✅ Bảo vệ các trang cần xác thực
- ✅ Quản lý session và redirect logic thông minh

### 2. Quản lý Sản phẩm
- ✅ Hiển thị danh sách sản phẩm với phân loại (Hot, New, Normal)
- ✅ Chi tiết sản phẩm với hình ảnh và thông tin đầy đủ
- ✅ Hệ thống giảm giá tự động dựa trên trạng thái sản phẩm
- ✅ Tìm kiếm sản phẩm theo tên và thương hiệu

### 3. Giỏ hàng và Thanh toán
- ✅ Giỏ hàng session-based cho khách hàng chưa đăng nhập
- ✅ Giỏ hàng user-based cho khách hàng đã đăng nhập
- ✅ Tính toán giá tự động với hệ thống giảm giá
- ✅ Hỗ trợ thanh toán online (MoMo QR) và thanh toán khi nhận hàng
- ✅ Quản lý đơn hàng với trạng thái real-time

### 4. AI Chatbot thông minh
- ✅ Gợi ý size quần áo dựa trên chiều cao và cân nặng
- ✅ Tìm kiếm sản phẩm theo danh mục (rẻ, đắt, hot, mới, giảm giá)
- ✅ Tương tác qua API JSON
- ✅ Xử lý lỗi và validation dữ liệu

### 5. Hệ thống Gợi ý Sản phẩm (Recommendation System)
- ✅ Thuật toán Apriori cho Association Rule Mining
- ✅ Phân tích hành vi mua hàng từ lịch sử đơn hàng
- ✅ Gợi ý sản phẩm liên quan dựa trên sản phẩm hiện tại
- ✅ Cache và tối ưu hiệu suất

### 6. Quản lý Đơn hàng
- ✅ Theo dõi trạng thái đơn hàng (Đang xử lý, Đang vận chuyển, Đã giao, Đã hủy)
- ✅ Lịch sử đơn hàng cho người dùng
- ✅ Hủy đơn hàng
- ✅ Tích hợp với GHN (Giao Hang Nhanh)

### 7. Giao diện người dùng
- ✅ Responsive design
- ✅ Blog và trang About
- ✅ Form liên hệ
- ✅ Hiển thị thông báo thành công/lỗi

## 🛠 Công nghệ sử dụng

### Backend
- **Django 4.x** - Web framework chính
- **SQLite** - Cơ sở dữ liệu
- **Django ORM** - Quản lý dữ liệu
- **Django Forms** - Xử lý form và validation

### AI & Machine Learning
- **Association Rule Mining** - Thuật toán Apriori
- **Product Recommendation System** - Hệ thống gợi ý sản phẩm
- **Size Recommendation** - Gợi ý size quần áo

### Frontend
- **HTML5/CSS3** - Giao diện người dùng
- **JavaScript** - Tương tác động
- **Bootstrap** - Framework CSS (nếu có)

### API & Integration
- **RESTful API** - Cho chatbot và AJAX requests
- **MoMo Payment** - Thanh toán online
- **GHN API** - Vận chuyển

## 📁 Cấu trúc dự án

```
IT-Challenge/
├── ecommerce_project/     # Django project settings
├── shop/                  # Main app
│   ├── models.py         # Database models
│   ├── views.py          # Business logic
│   ├── forms.py          # Form definitions
│   ├── urls.py           # URL routing
│   ├── recommendation.py # AI recommendation system
│   ├── chat.py           # AI chatbot
│   ├── tests.py          # Unit tests
│   ├── templates/        # HTML templates
│   └── static/           # Static files
├── db.sqlite3            # Database
├── manage.py             # Django management
└── README.md             # Project documentation
```

## 🚀 Cách chạy dự án

### 1. Cài đặt môi trường
```bash
# Tạo virtual environment
python -m venv venv

# Kích hoạt virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Cài đặt dependencies
pip install -r requirements.txt
```

### 2. Chạy migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Tạo superuser (tùy chọn)
```bash
python manage.py createsuperuser
```

### 4. Chạy server
```bash
python manage.py runserver
```

### 5. Truy cập ứng dụng
- **Website:** http://localhost:8000
- **Admin:** http://localhost:8000/admin

## 👤 Tài khoản demo

### Admin
- **Username:** tk
- **Password:** admin123

### User
- **Username:** hehe11 | **Password:** vinh123
- **Username:** congvinh | **Password:** 123

## 🧪 Testing

Chạy test cases:
```bash
python manage.py test shop.tests.AuthenticationTestCase
```

## 🔧 Tính năng nổi bật

### 1. Hệ thống Giảm giá Thông minh
- Tự động áp dụng giảm giá dựa trên trạng thái sản phẩm
- Sản phẩm "New": Giảm 10%
- Sản phẩm "Hot": Giảm 20%
- Tự động hết hạn sau 7 ngày

### 2. AI Recommendation System
- Phân tích hành vi mua hàng
- Gợi ý sản phẩm liên quan
- Sử dụng thuật toán Apriori với min_support=0.008, min_confidence=0.1

### 3. Smart Cart System
- Tính toán giảm giá theo tổng giá trị đơn hàng
- Giảm 10% cho đơn hàng ≥ 1,000,000 VNĐ
- Giảm 20% cho đơn hàng ≥ 3,000,000 VNĐ
- Giảm 30% cho đơn hàng ≥ 5,000,000 VNĐ
- Giới hạn giảm giá tối đa 2,500,000 VNĐ

### 4. AI Chatbot
- Gợi ý size quần áo dựa trên chiều cao/cân nặng
- Tìm kiếm sản phẩm theo danh mục
- API endpoints cho tương tác

## 📊 Database Schema

### Models chính:
- **Product:** Sản phẩm với thông tin chi tiết
- **Cart/CartItem:** Giỏ hàng và items
- **Order/OrderItem:** Đơn hàng và chi tiết
- **User:** Người dùng (Django built-in)
- **ContactForm:** Form liên hệ

## 🔒 Bảo mật

- ✅ CSRF protection
- ✅ Password hashing
- ✅ Session management
- ✅ Input validation
- ✅ SQL injection protection
- ✅ Authentication decorators

## 🚀 Deployment

Dự án có thể được deploy lên:
- Heroku
- PythonAnywhere
- DigitalOcean
- AWS

## 📝 Ghi chú phát triển

- Dự án được phát triển theo mô hình MVC
- Sử dụng Class-based Views cho authentication
- Function-based Views cho các chức năng khác
- Tích hợp AI/ML để tăng trải nghiệm người dùng
- Responsive design cho mobile-friendly

## 🤝 Đóng góp

Dự án này được phát triển bởi Đào Công Vinh (MSSV: 22130325) như một phần của IT Challenge.

---

**© 2024 Đào Công Vinh - MSSV: 22130325**