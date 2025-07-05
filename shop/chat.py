from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Product

# Gợi ý size dựa trên chiều cao và cân nặng
def recommend_size(height, weight):
    """Hàm đơn giản gợi ý size dựa trên chiều cao và cân nặng."""
    try:
        height = float(height)
        weight = float(weight)
    except ValueError:
        return "Chiều cao và cân nặng phải là số."

    if height < 165:
        if weight < 50:
            return "XS"
        elif weight <= 60:
            return "S"
        else:
            return "M"
    elif height < 175:
        if weight < 60:
            return "S"
        elif weight <= 75:
            return "M"
        else:
            return "L"
    elif weight < 180:
        if weight < 76:
            return "XL"
        elif weight <= 85:
            return "2XL"
        else:
            return "3XL"
    else:
        return "3XL"

@csrf_exempt
def size_chatbot(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            height = data.get("height")
            weight = data.get("weight")

            if not height or not weight:
                return JsonResponse({"success": False, "message": "Vui lòng cung cấp cả chiều cao và cân nặng."}, status=400)

            # Gợi ý size
            size = recommend_size(height, weight)
            return JsonResponse({"success": True, "size": size, "message": f"Gợi ý size của bạn là: {size}."})
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Dữ liệu gửi lên không hợp lệ."}, status=400)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "message": "Chỉ hỗ trợ phương thức POST."}, status=400)

@csrf_exempt
def get_products(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            category = data.get("category", "").lower()

            if not category:
                return JsonResponse({"success": False, "message": "Vui lòng cung cấp danh mục."}, status=400)

            # Lấy sản phẩm theo danh mục status
            if category == "cheap":
                products = Product.objects.order_by('price')[:5]  # Sản phẩm giá rẻ
            elif category == "expensive":
                products = Product.objects.order_by('-price')[:5]  # Sản phẩm đắt
            elif category == "hot":
                products = Product.objects.filter(status=Product.StatusChoices.HOT)[:5]  # Sản phẩm hot
            elif category == "new":
                products = Product.objects.filter(status=Product.StatusChoices.NEW)[:5]  # Sản phẩm mới
            elif category == "sales":
                products = Product.objects.filter(is_discounted=True)[:5]  # Sản phẩm đang giảm giá
            else:
                return JsonResponse({"success": False, "message": "Danh mục không hợp lệ."}, status=400)

            # Trả về danh sách sản phẩm dưới dạng JSON, chỉ chứa tên và giá
            product_list = [{"name": product.name, "price": product.get_current_price()} for product in products]
            return JsonResponse({"success": True, "products": product_list})

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Dữ liệu gửi lên không hợp lệ."}, status=400)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "message": "Chỉ hỗ trợ phương thức POST."}, status=400)