# shop/urls.py
from django.urls import include, path
from django.shortcuts import render
from . import views
from . import chat

def test_view(request):
    return render(request, 'shop/test.html')

urlpatterns = [
    path('', views.product_list_home, name='home'),
    path('test/', test_view, name='test'),
    path('login/', views.loginView.as_view(), name='login'),
    path('register/', views.register.as_view(), name='register'),
    path('logout/', views.logout_view, name='logout'),  # Thêm lại URL logout
    path('products/', views.product_list, name='shop'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('blog/', views.blog, name='blog'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('saveContact/', views.saveContact, name='saveContact'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('delete_item/<int:item_id>/', views.delete_cart_item, name='delete_cart_item'),
    path('update-cart-item/', views.update_cart_item, name='update_cart_item'),
    path("cart/total/", views.get_cart_total, name="cart_total"),
    path('search/', views.product_search, name='product_search'),
    path('payment/', views.payment, name='order_payment'),
    path('place_order/', views.place_order, name='place_order'),
    path('order/success/<int:order_id>/', views.order_detail, name='order_detail'),
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('order-history/', views.order_history, name='order_history'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('related_products/', views.related_products, name='related_products'),
    path('payment_scan/', views.payment_scan, name='payment_scan'),
    path('order_success/', views.order_success, name='order_success'),
    path('size-chatbot/', chat.size_chatbot, name='size_chatbot'),
    path('get-products/', chat.get_products, name='get_products'),
    path('check-payment-status/', views.check_payment_status, name='check_payment_status'),
    path('cart/items-count/', views.cart_items_count, name='cart_items_count'),
]
