# Hệ thống Authentication - BaRoiBeo E-commerce

## Tổng quan

Hệ thống authentication của BaRoiBeo bao gồm đăng ký, đăng nhập và đăng xuất với các tính năng sau:

- ✅ Đăng ký tài khoản mới
- ✅ Đăng nhập với username/password
- ✅ Đăng xuất
- ✅ Validation form đầy đủ
- ✅ Hiển thị thông báo lỗi/thành công
- ✅ Bảo vệ các trang cần authentication
- ✅ Redirect logic thông minh

## Các file chính

### 1. Forms (`shop/forms.py`)
- `RegisterForm`: Form đăng ký kế thừa từ `UserCreationForm`
- `LoginForm`: Form đăng nhập
- Validation cho username/email trùng lặp
- Validation mật khẩu

### 2. Views (`shop/views.py`)
- `loginView`: Class-based view xử lý đăng nhập
- `register`: Class-based view xử lý đăng ký  
- `logout_view`: Function view xử lý đăng xuất

### 3. Templates
- `login.html`: Trang đăng nhập
- `register.html`: Trang đăng ký
- `base.html`: Template cơ sở với hiển thị messages

### 4. URLs (`shop/urls.py`)
```python
path('login/', views.loginView.as_view(), name='login'),
path('register/', views.register.as_view(), name='register'),
path('logout/', views.logout_view, name='logout'),
```

## Tính năng chi tiết

### Đăng ký
- ✅ Validation username trùng lặp
- ✅ Validation email trùng lặp
- ✅ Validation mật khẩu (độ mạnh, xác nhận)
- ✅ Tự động redirect về trang login sau khi đăng ký thành công
- ✅ Hiển thị lỗi validation chi tiết

### Đăng nhập
- ✅ Validation thông tin đăng nhập
- ✅ Redirect về trang trước đó (next parameter)
- ✅ Redirect về trang chủ nếu không có next
- ✅ Hiển thị thông báo chào mừng
- ✅ Xử lý lỗi đăng nhập

### Đăng xuất
- ✅ Xóa session
- ✅ Redirect về trang chủ
- ✅ Hiển thị thông báo thành công

### Bảo mật
- ✅ CSRF protection
- ✅ Password hashing
- ✅ Session management
- ✅ Login required decorator cho các trang cần thiết

## Test Cases

Chạy test để kiểm tra:
```bash
python manage.py test shop.tests.AuthenticationTestCase
```

Test cases bao gồm:
- ✅ Form validation
- ✅ View responses
- ✅ User creation
- ✅ Login/logout flow
- ✅ Redirect logic
- ✅ Authentication checks

## Cách sử dụng

### 1. Đăng ký tài khoản mới
```
POST /register/
{
    "username": "newuser",
    "email": "user@example.com", 
    "password1": "securepass123",
    "password2": "securepass123"
}
```

### 2. Đăng nhập
```
POST /login/
{
    "username": "newuser",
    "password": "securepass123"
}
```

### 3. Đăng xuất
```
GET /logout/
```

### 4. Truy cập trang cần authentication
```python
from django.contrib.auth.decorators import login_required

@login_required
def protected_view(request):
    # Chỉ user đã đăng nhập mới truy cập được
    pass
```

## Cấu hình

### Settings (`ecommerce_project/settings.py`)
```python
# Không cần cấu hình đặc biệt cho authentication cơ bản
# Django sử dụng cấu hình mặc định
```

## Troubleshooting

### Lỗi thường gặp

1. **Form validation errors không hiển thị**
   - Kiểm tra template có render form errors không
   - Kiểm tra CSS cho error messages

2. **Redirect không hoạt động**
   - Kiểm tra next parameter trong URL
   - Kiểm tra view logic

3. **Session không lưu**
   - Kiểm tra SESSION_ENGINE trong settings
   - Kiểm tra database migrations

## Security Notes

- ✅ Passwords được hash bằng Django's built-in hashers
- ✅ CSRF protection enabled
- ✅ Session security
- ✅ Input validation và sanitization
- ✅ SQL injection protection (Django ORM)

## Future Improvements

- [ ] Email verification
- [ ] Password reset functionality  
- [ ] Two-factor authentication
- [ ] Account lockout after failed attempts
- [ ] Remember me functionality 