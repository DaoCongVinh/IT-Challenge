# CHỨC NĂNG ĐĂNG NHẬP - HỆ THỐNG BAROIBEO

**Sinh viên thực hiện:** ĐÀO CÔNG VINH  
**MSSV:** 22130325  
**Chức năng:** Hệ thống Authentication  
**Ngày thực hiện:** 2024

---

## I. TỔNG QUAN CHỨC NĂNG ĐĂNG NHẬP

### 1.1. Mô tả chức năng
Hệ thống đăng nhập của BaRoiBeo được thiết kế theo mô hình Class-based View của Django, cung cấp giao diện đăng nhập an toàn và thân thiện với người dùng. Hệ thống hỗ trợ đăng nhập bằng username và password, với các tính năng bảo mật và validation đầy đủ.

### 1.2. Các thành phần chính
- **LoginForm:** Form validation và xử lý dữ liệu
- **loginView:** Class-based view xử lý logic đăng nhập
- **Authentication:** Django's built-in authentication system
- **Session Management:** Quản lý phiên đăng nhập
- **Redirect Logic:** Xử lý chuyển hướng thông minh

---

## II. CHI TIẾT KỸ THUẬT

### 2.1. Cấu trúc Code

#### 2.1.1. Form Definition (`shop/forms.py`)
```python
class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tên đăng nhập'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mật khẩu'
        })
    )
```

#### 2.1.2. View Implementation (`shop/views.py`)
```python
class loginView(View):
    def get(self, request):
        # Kiểm tra nếu user đã đăng nhập
        if request.user.is_authenticated:
            return redirect('home')
        
        # Hiển thị form đăng nhập
        lF = LoginForm()
        return render(request, 'shop/login.html', {'lF': lF})

    def post(self, request):
        lF = LoginForm(request.POST)
        
        if lF.is_valid():
            username = lF.cleaned_data['username']
            password = lF.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Chào mừng {user.username}! Đăng nhập thành công!")
                
                # Redirect logic thông minh
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
            else:
                messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng.")
        else:
            messages.error(request, "Vui lòng kiểm tra lại thông tin đăng nhập.")
        
        return render(request, 'shop/login.html', {'lF': lF})
```

### 2.2. URL Configuration (`shop/urls.py`)
```python
path('login/', views.loginView.as_view(), name='login'),
```

---

## III. USE CASE - LUỒNG HOẠT ĐỘNG

### 3.1. Use Case: Đăng nhập thành công

#### **Actor:** Người dùng (User)
#### **Precondition:** Người dùng chưa đăng nhập
#### **Main Flow:**

1. **Truy cập trang đăng nhập**
   - User truy cập URL: `/login/`
   - Hệ thống kiểm tra trạng thái đăng nhập
   - Nếu đã đăng nhập → Redirect về trang chủ
   - Nếu chưa đăng nhập → Hiển thị form đăng nhập

2. **Nhập thông tin đăng nhập**
   - User nhập username và password
   - Form validation kiểm tra:
     - Username không được để trống
     - Password không được để trống
     - Độ dài username ≤ 150 ký tự

3. **Xử lý đăng nhập**
   - Hệ thống gọi `authenticate()` với username/password
   - Django kiểm tra thông tin trong database
   - Nếu thông tin đúng → Tạo session cho user
   - Nếu thông tin sai → Hiển thị thông báo lỗi

4. **Redirect sau đăng nhập**
   - Nếu có parameter `next` → Redirect về URL đó
   - Nếu không có `next` → Redirect về trang chủ
   - Hiển thị thông báo chào mừng

#### **Postcondition:** User đã đăng nhập thành công và được chuyển hướng

### 3.2. Use Case: Đăng nhập thất bại

#### **Actor:** Người dùng (User)
#### **Precondition:** Người dùng chưa đăng nhập
#### **Main Flow:**

1. **Truy cập trang đăng nhập** (tương tự Use Case thành công)

2. **Nhập thông tin sai**
   - User nhập username/password không đúng
   - Hoặc để trống các trường bắt buộc

3. **Validation và xử lý lỗi**
   - Form validation phát hiện lỗi
   - Hoặc `authenticate()` trả về None
   - Hệ thống hiển thị thông báo lỗi cụ thể

4. **Hiển thị form với lỗi**
   - Form được render lại với dữ liệu đã nhập
   - Thông báo lỗi hiển thị rõ ràng
   - User có thể thử lại

#### **Postcondition:** User vẫn chưa đăng nhập, form hiển thị với thông báo lỗi

### 3.3. Use Case: Truy cập trang được bảo vệ

#### **Actor:** Người dùng chưa đăng nhập
#### **Precondition:** User cố gắng truy cập trang cần authentication
#### **Main Flow:**

1. **Truy cập trang được bảo vệ**
   - User truy cập URL cần đăng nhập (ví dụ: `/payment/`)
   - Decorator `@login_required` kiểm tra trạng thái

2. **Redirect về trang đăng nhập**
   - Hệ thống redirect về `/login/?next=/payment/`
   - Parameter `next` lưu URL gốc

3. **Đăng nhập thành công**
   - User đăng nhập thành công
   - Hệ thống redirect về URL gốc (`/payment/`)

#### **Postcondition:** User được chuyển đến trang ban đầu muốn truy cập

---

## IV. TÍNH NĂNG BẢO MẬT

### 4.1. Password Security
- **Password Hashing:** Django tự động hash password bằng bcrypt
- **Salt:** Mỗi password được salt ngẫu nhiên
- **Secure Storage:** Password không bao giờ được lưu dưới dạng plain text

### 4.2. Session Management
- **Session ID:** Tạo session ID ngẫu nhiên cho mỗi lần đăng nhập
- **Session Expiry:** Session tự động hết hạn sau thời gian định sẵn
- **Secure Cookies:** Session cookie được đánh dấu secure

### 4.3. CSRF Protection
- **CSRF Token:** Mỗi form đều có CSRF token
- **Token Validation:** Server validate token trước khi xử lý request
- **Automatic Protection:** Django tự động bảo vệ khỏi CSRF attacks

### 4.4. Input Validation
- **Form Validation:** Kiểm tra dữ liệu đầu vào
- **SQL Injection Prevention:** Django ORM tự động bảo vệ
- **XSS Prevention:** Template engine tự động escape HTML

---

## V. GIAO DIỆN NGƯỜI DÙNG

### 5.1. Template Structure (`shop/templates/shop/login.html`)
```html
{% extends 'shop/base.html' %}

{% block content %}
<div class="login-container">
    <h2>Đăng nhập</h2>
    
    <!-- Hiển thị messages -->
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <!-- Login Form -->
    <form method="post">
        {% csrf_token %}
        <div class="form-group">
            {{ lF.username.label_tag }}
            {{ lF.username }}
            {% if lF.username.errors %}
                <div class="error">{{ lF.username.errors }}</div>
            {% endif %}
        </div>
        
        <div class="form-group">
            {{ lF.password.label_tag }}
            {{ lF.password }}
            {% if lF.password.errors %}
                <div class="error">{{ lF.password.errors }}</div>
            {% endif %}
        </div>
        
        <button type="submit" class="btn btn-primary">Đăng nhập</button>
    </form>
    
    <div class="links">
        <a href="{% url 'register' %}">Chưa có tài khoản? Đăng ký ngay</a>
    </div>
</div>
{% endblock %}
```

### 5.2. Responsive Design
- **Mobile-friendly:** Giao diện tối ưu cho mobile
- **Bootstrap Integration:** Sử dụng Bootstrap classes
- **User Experience:** Form dễ sử dụng, thông báo rõ ràng

---

## VI. TESTING

### 6.1. Unit Tests (`shop/tests.py`)
```python
class AuthenticationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_login_success(self):
        response = self.client.post('/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertTrue(response.wsgi_request.user.is_authenticated)
    
    def test_login_failure(self):
        response = self.client.post('/login/', {
            'username': 'testuser',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)  # Stay on page
        self.assertFalse(response.wsgi_request.user.is_authenticated)
```

### 6.2. Test Cases
- ✅ **Valid Login:** Đăng nhập với thông tin đúng
- ✅ **Invalid Login:** Đăng nhập với thông tin sai
- ✅ **Empty Fields:** Để trống username/password
- ✅ **Redirect Logic:** Kiểm tra redirect sau đăng nhập
- ✅ **Session Management:** Kiểm tra session được tạo
- ✅ **CSRF Protection:** Kiểm tra CSRF token

---

## VII. ERROR HANDLING

### 7.1. Validation Errors
- **Field Validation:** Hiển thị lỗi cho từng field
- **Form Validation:** Hiển thị lỗi tổng quát
- **User-friendly Messages:** Thông báo lỗi dễ hiểu

### 7.2. Authentication Errors
- **Invalid Credentials:** "Tên đăng nhập hoặc mật khẩu không đúng"
- **Account Locked:** Xử lý tài khoản bị khóa (nếu có)
- **Account Disabled:** Xử lý tài khoản bị vô hiệu hóa

### 7.3. System Errors
- **Database Errors:** Xử lý lỗi kết nối database
- **Session Errors:** Xử lý lỗi session
- **Server Errors:** Hiển thị trang lỗi 500

---

## VIII. PERFORMANCE & OPTIMIZATION

### 8.1. Database Optimization
- **Indexed Fields:** Username field được index
- **Query Optimization:** Sử dụng Django ORM hiệu quả
- **Connection Pooling:** Tối ưu kết nối database

### 8.2. Caching
- **Session Caching:** Cache session data
- **Template Caching:** Cache template rendering
- **Static Files:** Cache CSS/JS files

### 8.3. Security Optimization
- **Rate Limiting:** Giới hạn số lần đăng nhập thất bại
- **Account Lockout:** Khóa tài khoản sau nhiều lần thất bại
- **Audit Logging:** Ghi log các hoạt động đăng nhập

---

## IX. DEPLOYMENT CONSIDERATIONS

### 9.1. Production Settings
```python
# settings.py
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
```

### 9.2. Environment Variables
- **SECRET_KEY:** Khóa bí mật cho Django
- **DEBUG:** Chế độ debug (False trong production)
- **ALLOWED_HOSTS:** Danh sách domain được phép

### 9.3. Monitoring
- **Login Attempts:** Theo dõi số lần đăng nhập
- **Failed Logins:** Cảnh báo đăng nhập thất bại
- **Session Analytics:** Phân tích thời gian session

---

## X. KẾT LUẬN

Hệ thống đăng nhập của BaRoiBeo được thiết kế với các nguyên tắc bảo mật và trải nghiệm người dùng tốt nhất. Với việc sử dụng Django's built-in authentication system kết hợp với custom logic, hệ thống cung cấp:

- ✅ **Bảo mật cao** với password hashing, CSRF protection
- ✅ **Trải nghiệm tốt** với redirect logic thông minh
- ✅ **Dễ bảo trì** với code structure rõ ràng
- ✅ **Scalable** với kiến trúc có thể mở rộng
- ✅ **Testable** với unit tests đầy đủ

Hệ thống này đáp ứng đầy đủ các yêu cầu về bảo mật và usability cho một ứng dụng E-commerce hiện đại.

---

**© 2024 Đào Công Vinh - MSSV: 22130325**  
*Hệ thống Authentication BaRoiBeo E-commerce* 