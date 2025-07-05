from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import RegisterForm, LoginForm

# Create your tests here.

class AuthenticationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        
    def test_register_form_valid(self):
        """Test register form với dữ liệu hợp lệ"""
        form = RegisterForm(data=self.user_data)
        self.assertTrue(form.is_valid())
        
    def test_register_form_password_mismatch(self):
        """Test register form với mật khẩu không khớp"""
        data = self.user_data.copy()
        data['password2'] = 'wrongpassword'
        form = RegisterForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        
    def test_register_form_duplicate_username(self):
        """Test register form với username đã tồn tại"""
        # Tạo user trước
        User.objects.create_user(username='testuser', email='existing@example.com', password='testpass123')
        
        form = RegisterForm(data=self.user_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        
    def test_register_view_get(self):
        """Test register view với GET request"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/register.html')
        
    def test_register_view_post_valid(self):
        """Test register view với POST request hợp lệ"""
        response = self.client.post(reverse('register'), self.user_data)
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertRedirects(response, reverse('login'))
        
        # Kiểm tra user đã được tạo
        user = User.objects.get(username='testuser')
        self.assertEqual(user.email, 'test@example.com')
        
    def test_login_form_valid(self):
        """Test login form với dữ liệu hợp lệ"""
        # Tạo user trước
        User.objects.create_user(username='testuser', password='testpass123')
        
        form_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_login_view_get(self):
        """Test login view với GET request"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/login.html')
        
    def test_login_view_post_valid(self):
        """Test login view với POST request hợp lệ"""
        # Tạo user trước
        User.objects.create_user(username='testuser', password='testpass123')
        
        form_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(reverse('login'), form_data)
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertRedirects(response, reverse('home'))
        
    def test_login_view_post_invalid(self):
        """Test login view với thông tin đăng nhập sai"""
        form_data = {
            'username': 'wronguser',
            'password': 'wrongpass'
        }
        response = self.client.post(reverse('login'), form_data)
        self.assertEqual(response.status_code, 200)  # Không redirect
        self.assertTemplateUsed(response, 'shop/login.html')
        
    def test_logout_view(self):
        """Test logout view"""
        # Tạo và đăng nhập user
        user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')
        
        # Test logout
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertRedirects(response, reverse('home'))
        
        # Kiểm tra user đã logout
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        
    def test_authenticated_user_redirect(self):
        """Test user đã đăng nhập bị redirect khi truy cập login/register"""
        # Tạo và đăng nhập user
        user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')
        
        # Test redirect khi truy cập login
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        
        # Test redirect khi truy cập register
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
