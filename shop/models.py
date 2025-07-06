# models.py
from datetime import timedelta
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from random import randint, choice


class Product(models.Model):
    class StatusChoices(models.TextChoices):
        HOT = 'Hot', 'Hot'
        NEW = 'New', 'New'
        NORMAL = 'Normal', 'Normal'
        
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)
    image_url = models.URLField() 
    price = models.DecimalField(max_digits=10, decimal_places=0)
    is_discounted = models.BooleanField(default=False) #Có đang giảm giá hay không
    discounted_percent = models.PositiveIntegerField(default = 0) #Phần trăm giảm
    discounted_price = models.DecimalField(max_digits=10, decimal_places=0, default=0) #Giá sau khi giảm
    discount_start_date = models.DateTimeField(null=True, blank=True) #Ngày bắt đầu giảm giá
    description = models.TextField(blank=True, null=True) 
    rating = models.IntegerField()
    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.NORMAL,  # Default status
    )
    
    @property
    def formatted_price(self):
        return f"{self.price:,.0f}".replace(',', '.')
    
    @property
    def formatted_discounted_price(self):
        return f"{self.discounted_price:,.0f}".replace(',', '.')
    
    def check_discount_expiry(self):
        if self.is_discounted and self.discount_start_date:
            if timezone.now() - self.discount_start_date > timedelta(days=7):
                self.remove_discount()
                return True
        return False
    
    def check_status_for_discount(self):
        self.check_discount_expiry()
        
        if not self.is_discounted:
            if self.status == self.StatusChoices.NEW:
                self.discounted_percent = 10
                self.discounted_price = (self.price * Decimal(0.9)).quantize(Decimal('1'))
                self.is_discounted = True
                self.discount_start_date = timezone.now()
            elif self.status == self.StatusChoices.HOT:
                self.discounted_percent = 20
                self.discounted_price = (self.price * Decimal(0.8)).quantize(Decimal('1'))
                self.is_discounted = True
                self.discount_start_date = timezone.now()
            else:
                self.discounted_percent = 0
                self.discounted_price = self.price
                self.is_discounted = False
                self.discount_start_date = None
            
    def remove_discount(self):
        #Bỏ giảm giá
        self.is_discounted = False
        self.discounted_percent = 0
        self.discounted_price = self.price
        self.discount_start_date = None
        self.status = self.StatusChoices.NORMAL
        self.save()
    
    def apply_discount(self, percentage):
        self.check_discount_expiry() 
        self.discounted_percent = percentage
        self.discounted_price = (self.price * Decimal(1 - percentage / 100))
        self.is_discounted = True
        self.discount_start_date = timezone.now()
        
    def get_current_price(self):
        # Hiển thị lên giá giảm nếu có, nếu không thì hiển thị giá gốc
        self.check_discount_expiry()
        if self.is_discounted:
            return self.discounted_price
        else:
            return self.price

    def save(self, *args, **kwargs):
        self.check_status_for_discount()
        super().save(*args, **kwargs)

    def has_changed(self, field):
        """Check if a specific field has changed."""
        if not self.pk:
            return False
        old_value = Product.objects.filter(pk=self.pk).values_list(field, flat=True).first()
        new_value = getattr(self, field)
        return old_value != new_value

    def get_total_sold(self):
        """Tính tổng số lượng sản phẩm đã bán"""
        return OrderItem.objects.filter(product=self).aggregate(total_sold=models.Sum('quantity'))['total_sold'] or 0
    
    def __str__(self):
        return self.name

class Cart(models.Model):
    session = models.CharField(max_length=255, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.session or (self.user.username if self.user else 'Anonymous')}"

    def get_cart_total(self):
        return sum(item.get_total_price() for item in self.items.all()) if self.items.exists() else 0
    
    def get_cart_real_total(self):
        total = self.get_cart_total()
        discount = self.get_discount_amount()
        return max(total - discount, Decimal('0'))

    def get_cart_items_count(self):
        return self.items.count()
    
    def get_discount_percentage(self):
        total = self.get_cart_total()
        if total >= Decimal('5000000'):
            return Decimal('0.30')
        elif total >= Decimal('3000000'):
            return Decimal('0.20')
        elif total >= Decimal('1000000'):
            return Decimal('0.10')
        else:
            return Decimal('0')

    def get_discount_amount(self, payment_method=None):
        total = self.get_cart_total()
        discount_percentage = self.get_discount_percentage()
        discount_amount = total * discount_percentage
        
        # Cap the discount at 2.5 million
        discount_amount = min(discount_amount, Decimal('2500000'))
            
        return discount_amount



class CartItem(models.Model):
    """Từng sản phẩm trong giỏ hàng"""
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    size = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    
    class Meta:
        unique_together = ('cart', 'product', 'size')

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_total_price(self):
        if (self.product.is_discounted):
            return self.quantity * self.product.discounted_price
        else:
            return self.quantity * self.product.get_current_price()
    
    def formatted_total_price(self):
        return f"{self.get_total_price():,.0f}".replace(",", ".")
    
    def update_quantity(self, quantity):
        """Update the quantity and save."""
        if quantity > 0:
            self.quantity = quantity
            self.save()
        else:
            self.delete()
    
class ContactForm(models.Model):
    username = models.CharField(max_length = 25)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.username


class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Đang xử lý'),
        ('Shipping', 'Đang vận chuyển'),
        ('Delivered', 'Đã giao thành công'),
        ('Cancelled', 'Đã hủy'),
    ]

    PAYMENT_CHOICES = [
        ('COD', 'Thanh toán khi nhận hàng (COD)'),
        ('MoMo', 'Thanh toán online bằng quét mã QR'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    note = models.TextField(blank=True, null=True)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    total_price = models.DecimalField(max_digits=20, decimal_places=0, default=0)  # Thêm trường này
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Pending')  # Thêm trường trạng thái
    ghn_order_code = models.CharField(max_length=32, blank=True, null=True, help_text="Mã vận đơn GHN")

    def __str__(self):
        return f"Order by {self.user.username} - {self.payment_method}"

    def get_total_price(self):
        """Get total price including discounts"""
        return self.total_price

    def get_subtotal(self):
        """Get the total before discounts"""
        return sum(item.get_total_price() for item in self.items.all())

    def get_discount_amount(self):
        """Calculate the discount amount"""
        subtotal = self.get_subtotal()
        # Apply the same discount logic as cart
        if subtotal >= Decimal('5000000'):
            return min(subtotal * Decimal('0.30'), Decimal('2500000'))
        elif subtotal >= Decimal('3000000'):
            return min(subtotal * Decimal('0.20'), Decimal('2500000'))
        elif subtotal >= Decimal('1000000'):
            return min(subtotal * Decimal('0.10'), Decimal('2500000'))
        return Decimal('0')

    def get_final_total(self):
        """Get the final total after discounts"""
        return self.get_subtotal() - self.get_discount_amount()
    
    def is_online_payment(self):
        return self.payment_method == 'MoMo'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.total_price = self.get_total_price()
        super().save(update_fields=['total_price'])


class Address(models.Model):
    """Model lưu thông tin địa chỉ chi tiết từ API provinces.open-api.vn"""
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='address_detail')
    province_code = models.CharField(max_length=10, blank=True, null=True)
    province_name = models.CharField(max_length=100, blank=True, null=True)
    district_code = models.CharField(max_length=10, blank=True, null=True)
    district_name = models.CharField(max_length=100, blank=True, null=True)
    ward_code = models.CharField(max_length=10, blank=True, null=True)
    ward_name = models.CharField(max_length=100, blank=True, null=True)
    address_detail = models.CharField(max_length=255, blank=True, null=True)
    
    def get_full_address(self):
        """Trả về địa chỉ đầy đủ"""
        parts = []
        if self.address_detail:
            parts.append(self.address_detail)
        if self.ward_name:
            parts.append(self.ward_name)
        if self.district_name:
            parts.append(self.district_name)
        if self.province_name:
            parts.append(self.province_name)
        return ', '.join(parts)
    
    def __str__(self):
        return f"Địa chỉ đơn hàng #{self.order.id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=20, decimal_places=0)

    def get_total_price(self):
        return self.quantity * self.price  # Tổng tiền = Số lượng * Đơn giá

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}"
