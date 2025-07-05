from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import ContactForm

class Contact_Form(forms.ModelForm):
    class Meta:
        model = ContactForm
        fields = ['username', 'email', 'subject', 'message']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Nhập tên của bạn', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'E-mail', 'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Tiêu đề', 'class': 'form-control'}),
            'message': forms.Textarea(attrs={'placeholder': 'Lời nhắn', 'cols': 30, 'rows': 10, 'class': 'form-control'}),
        }

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email *', 'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Tên tài khoản *', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Mật khẩu *',
            'class': 'form-control'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Nhập lại mật khẩu *',
            'class': 'form-control'
        })
        # Xóa help text mặc định
        for field in self.fields.values():
            field.help_text = ''

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Tên tài khoản này đã tồn tại.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email này đã được sử dụng.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Mật khẩu và xác nhận mật khẩu không khớp.")

        return cleaned_data
    
class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Tên tài khoản *',
            'class': 'form-control',
            'id': 'id_username'
        })
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Mật khẩu *',
            'class': 'form-control',
            'id': 'id_password'
        })
    )
    
class PaymentForm(forms.Form):
    name = forms.CharField(max_length=100, label="Tên")
    phone = forms.CharField(max_length=15, label="Điện thoại liên lạc")
    address = forms.CharField(max_length=255, label="Địa chỉ")
    note = forms.CharField(widget=forms.Textarea, required=False, label="Ghi chú")
    payment = forms.ChoiceField(
        choices=[('COD', 'Thanh toán khi nhận hàng (COD)'), ('MoMo', 'Thanh toán bằng ví MoMo')],
        label="Phương thức thanh toán",
        widget=forms.RadioSelect
    )