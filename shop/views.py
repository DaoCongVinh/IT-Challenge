from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import Sum


# views.py
from .recommendation import ProductRecommendation

from .models import Product,ContactForm,Cart,CartItem,Order,OrderItem
from .forms import Contact_Form , RegisterForm , LoginForm,PaymentForm
import json
from django.views import View
from django.contrib.auth.models import User
from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

import openai
import os
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect

# ========================================
# LOGOUT VIEW - Xử lý đăng xuất người dùng
# ========================================
def logout_view(request):
    """
    View function để xử lý đăng xuất người dùng
    - Gọi auth_logout() để xóa session
    - Redirect về trang login
    - Hoạt động với cả GET và POST request
    """
    auth_logout(request)  # Xóa session của user
    messages.success(request, "Đăng xuất thành công!")
    return redirect('home')  # Chuyển về trang chủ thay vì login

def homePage(request):
    return render(request, 'shop/homePage.html')

class loginView(View):
    def get(self, request):
        # Nếu user đã đăng nhập, redirect về trang chủ
        if request.user.is_authenticated:
            return redirect('home')
        
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
                
                # Redirect về trang trước đó hoặc trang chủ
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
            else:
                messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng.")
        else:
            messages.error(request, "Vui lòng kiểm tra lại thông tin đăng nhập.")
        
        return render(request, 'shop/login.html', {'lF': lF})

class register(View): #use class base view 
    def get(self, request):
        # Nếu user đã đăng nhập, redirect về trang chủ
        if request.user.is_authenticated:
            return redirect('home')
        
        rF = RegisterForm() 
        return render(request, 'shop/register.html', {'rF': rF})

    def post(self, request):
        rF = RegisterForm(request.POST) 

        if rF.is_valid():
            try:
                user = rF.save(commit=False)
                user.email = rF.cleaned_data['email']
                user.save()
                
                messages.success(request, "Đăng ký thành công! Vui lòng đăng nhập.")
                return redirect('login')
            except Exception as e:
                messages.error(request, f"Lỗi khi tạo tài khoản: {str(e)}")
        else:
            # Hiển thị lỗi validation
            for field, errors in rF.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
        
        return render(request, 'shop/register.html', {'rF': rF})

def product_list(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'shop/product.html', context)

def product_list_home(request):
    # Lấy sản phẩm bán chạy nhất
    hot_products = Product.objects.annotate(total_sold=Sum('orderitem__quantity')).order_by('-total_sold')[:10]  # Top 10 sản phẩm bán chạy nhất
    
    # Lấy sản phẩm mới
    new_products = Product.objects.filter(status=Product.StatusChoices.NEW)[:10]  # Giới hạn 10 sản phẩm mới
    
    # Lấy sản phẩm bình thường
    normal_products = Product.objects.filter(status=Product.StatusChoices.NORMAL)[:10]
    
    context = {
        'hot_products': hot_products,
        'new_products': new_products,
        'normal_products': normal_products
    }
    return render(request, 'shop/homePage.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Lấy sản phẩm được đề xuất
    recommendations = ProductRecommendation.get_recommendations_for_product(product)
    
    context = {
        'product': product,
        'related_products': recommendations
    }
    return render(request, 'shop/product_detail.html', context)


def blog(request):
    blog_posts = [
        {
            "title": "The Cotton Jersey Zip-Up Hoodie",
            "content": "The Cotton Jersey Zip-Up Hoodie is a versatile and comfortable outerwear piece that combines style and functionality. Crafted from high-quality cotton jersey fabric, this hoodie offers a cozy feel and a casual yet fashionable look.",
            "image": "/img/blog/b1.jpg",
            "date": "13/01"
        },
        {
            "title": "How to Style a Quiff",
            "content": "The Quiff is a timeless and sophisticated hairstyle that never fails to make a statement. With its voluminous and sculpted front, it adds a touch of elegance and charm to any look.",
            "image": "img/blog/b2.jpg",
            "date": "13/04"
        },
                {
            "title": "The Cotton Jersey Zip-Up Hoodie",
            "content": "The Cotton Jersey Zip-Up Hoodie is a versatile and comfortable outerwear piece that combines style and functionality. Crafted from high-quality cotton jersey fabric, this hoodie offers a cozy feel and a casual yet fashionable look.",
            "image": "/img/blog/b1.jpg",
            "date": "13/01"
        },
        {
            "title": "How to Style a Quiff",
            "content": "The Quiff is a timeless and sophisticated hairstyle that never fails to make a statement. With its voluminous and sculpted front, it adds a touch of elegance and charm to any look.",
            "image": "img/blog/b2.jpg",
            "date": "13/04"
        },
        
        # Add more posts here
    ]
    return render(request, 'shop/blog.html', {'blog_posts': blog_posts})

def about(request):
    return render(request, 'shop/about.html')

# get input from forms to save as models 
def contact(request):
    cf = Contact_Form()
    return render(request, 'shop/contact.html' , {'cf':cf})

def saveContact(request):
    print("Request received at saveContact")  # Kiểm tra xem view có được gọi không
    if request.method == "POST":
        cf = Contact_Form(request.POST)
        if cf.is_valid():
            saveCF = ContactForm(
                username=cf.cleaned_data['username'],
                email=cf.cleaned_data['email'],
                subject=cf.cleaned_data['subject'],
                message=cf.cleaned_data['message']
            )
            saveCF.save()
            return HttpResponse("save success")
    else:
        return HttpResponse("not POST")
            
def cart(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        cart, created = Cart.objects.get_or_create(session=session_key)

    discount = f"{cart.get_discount_amount():,.0f}".replace(",", ".")
    total = f"{cart.get_cart_total():,.0f}".replace(",", ".")
    real_total = f"{(float(total.replace(".","")) - float(discount.replace(".",""))):,.0f}".replace(",", ".")

    context = {
        "cart": cart,
        "discount": discount,
        "total": total,
        "real_total": real_total
    }
    return render(request, "shop/cart.html", context)

@csrf_exempt
def add_to_cart(request):
    if request.method == "POST":
        data = json.loads(request.body)
        product_id = data.get("product_id")
        size = data.get("size")

        print(f"Add to cart - Product ID: {product_id}, Size: {size}")

        # Chỉ chấp nhận size hợp lệ
        valid_sizes = ["M", "L", "XL", "XXL"]
        if not size or size not in valid_sizes:
            return JsonResponse({"success": False, "error": "Vui lòng chọn size"}, status=400)

        try:
            # Get the product
            product = get_object_or_404(Product, id=product_id)

            # Get or create the cart
            if request.user.is_authenticated:
                cart, created = Cart.objects.get_or_create(user=request.user)
            else:
                session_id = request.session.session_key
                if not session_id:
                    request.session.create()
                    session_id = request.session.session_key
                cart, created = Cart.objects.get_or_create(session=session_id)

            print(f"Cart retrieved - ID: {cart.id}, Created: {created}, Session: {session_id if not request.user.is_authenticated else 'User authenticated'}")

            # Check if a CartItem with the same product and size exists
            cart_item, item_created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                size=size,
                defaults={"quantity": 1}
            )

            print(f"Cart Item - Created: {item_created}, Quantity: {cart_item.quantity}")

            if not item_created:
                # If the item exists, increment the quantity
                cart_item.quantity += 1
                cart_item.save()

            # Verify cart items
            cart_items_count = cart.get_cart_items_count()
            print(f"Cart items count: {cart_items_count}")

            # Return a success response
            return JsonResponse({
                "success": True,
                "product_name": product.name,
                "size": size,
                "quantity": cart_item.quantity,
                "cart_total": cart.get_cart_total(),
                "cart_items_count": cart_items_count
            })
        except Exception as e:
            print(f"Error adding to cart: {str(e)}")
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Invalid request method"}, status=400)

def delete_cart_item(request, item_id):
    if request.method == "GET" and request.headers.get("X-Requested-With") == "XMLHttpRequest":
        try:
            cart_item = get_object_or_404(CartItem, id=item_id)
            cart = cart_item.cart
            cart_item.delete()
            cart_total = cart.get_cart_total()
            return JsonResponse({"success": True, "cart_total": cart_total})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    return JsonResponse({"success": False, "message": "Invalid request"})

def update_cart_item(request):
    """Update cart item quantity."""
    try:
        data = json.loads(request.body)
        cart_id = data.get('cart_id')
        product_id = data.get('product_id')
        item_id = data.get('item_id')
        quantity = int(data.get('quantity', 1))

        cart_item = CartItem.objects.get(id=item_id, cart_id=cart_id, product_id=product_id)
        cart_item.update_quantity(quantity)

        return JsonResponse({
            'success': True,
            'item_total_price': f"{cart_item.get_total_price():,.0f}".replace(",", "."),
            'cart_total': f"{cart_item.cart.get_cart_total():,.0f}".replace(",", "."),
            'discount_amount': f"{cart_item.cart.get_discount_amount():,.0f}".replace(",", "."),
            'cart_real_total': f"{cart_item.cart.get_cart_real_total():,.0f}".replace(",", "."),
            'cart_items_count': cart_item.cart.get_cart_items_count(),
        })
    except CartItem.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Cart item not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@csrf_exempt
def get_cart_total(request):
    try:
        session_key = request.session.session_key
        if not session_key:
            return JsonResponse({"success": False, "message": "Cart not found."}, status=404)

        cart = Cart.objects.get(session=session_key)
        cart_total = cart.get_cart_total()
        return JsonResponse({"success": True, "cart_total": cart_total})
    except Cart.DoesNotExist:
        return JsonResponse({"success": False, "message": "Cart not found."}, status=404)
    
def product_search(request):
    query = request.GET.get('search', '')
    page = request.GET.get('page', 1)
    
    if query :
        pattern = '.*' + '.*'.join(query.split()) + '.*'
        
        products_list = Product.objects.filter(
            Q(name__iregex=pattern) | Q(brand__iregex=pattern)
        )
    else :
        products_list = Product.objects.all()
    
    paginator = Paginator(products_list, 20)  # 20 products per page
    products = paginator.get_page(page)
    
    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'shop/product.html', context)

def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        cart, created = Cart.objects.get_or_create(session=session_id)
    
    print(f"Cart created: {created}, Cart ID: {cart.id}, Session: {request.session.session_key}, User: {request.user.username}")
    return cart

 # Hiện form thông tin thanh toán 
def payment(request):
    cart = get_or_create_cart(request)

    if request.method == 'POST':
        return place_order(request)

    form = PaymentForm()
    return render(request, 'shop/cart.html', {'cart': cart, 'form': form})

# Đảm bảo hàm place_order tồn tại và chỉ lưu đơn hàng local
@login_required
def place_order(request):
    cart = get_or_create_cart(request)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']
            note = form.cleaned_data.get('note', '')
            payment_method = form.cleaned_data['payment']

            real_total = cart.get_cart_real_total()

            order = Order.objects.create(
                user=request.user,
                name=name,
                phone=phone,
                address=address,
                note=note,
                payment_method=payment_method,
                total_price=real_total
            )
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    size=item.size,
                    quantity=item.quantity,
                    price=item.product.get_current_price()
                )
            cart.items.all().delete()
            print(f"Order created local only: {order.id}")
            return redirect('order_detail', order_id=order.id)

        return JsonResponse({'success': False, 'errors': form.errors})

    return JsonResponse({'success': False, 'message': 'Invalid request'})


#order detail
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    print(f"Order total price: {order.total_price}")
    return render(request, 'shop/order_detail.html', {'order': order})

#lich su don hang:
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shop/order_history.html', {'orders': orders})

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if request.method == 'POST':
        order.delete()
        messages.success(request, f"Đơn hàng #{order_id} đã được hủy thành công.")
        return redirect('order_history')  # Hoặc trang bạn muốn chuyển đến sau khi hủy

    return render(request, 'shop/order_cancel.html', {'order': order})

def payment_scan(request):
    return render(request, 'shop/payment_scan.html')

def order_success(request):
    return render(request, 'shop/order_success.html')

def payment_success(request): 
    return render(request, 'shop/payment_success.html')

def related_products(request):
    return render(request, 'shop/related_products.html')

@csrf_exempt
def check_payment_status(request):
    
    payment_success = False

    if request.session.get('payment_confirmed', False):
        payment_success = True

    return JsonResponse({'payment_success': payment_success})

def cart_items_count(request):
    count = 0
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart = Cart.objects.filter(session=session_key).first()
    if cart:
        count = cart.get_cart_items_count()
    return JsonResponse({'cart_items_count': count})
