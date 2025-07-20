import hashlib
import hmac
import urllib.parse
from django.conf import settings

def build_vnpay_url(order_id, amount, client_ip, return_url):
    vnp_TmnCode = settings.VNPAY_TMN_CODE
    vnp_HashSecret = settings.VNPAY_HASH_SECRET
    vnp_Url = settings.VNPAY_URL
    vnp_ReturnUrl = return_url

    vnp_Params = {
        'vnp_Version': '2.1.0',
        'vnp_Command': 'pay',
        'vnp_TmnCode': vnp_TmnCode,
        'vnp_Amount': str(int(amount) * 100),  # VNPAY yêu cầu nhân 100
        'vnp_CurrCode': 'VND',
        'vnp_TxnRef': str(order_id),
        'vnp_OrderInfo': f'Thanh toan don hang {order_id}',
        'vnp_OrderType': 'other',
        'vnp_Locale': 'vn',
        'vnp_ReturnUrl': vnp_ReturnUrl,
        'vnp_IpAddr': client_ip,
    }
    import datetime
    vnp_Params['vnp_CreateDate'] = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    # Sắp xếp các tham số theo thứ tự alphabet
    sorted_params = sorted(vnp_Params.items())
    query_string = '&'.join([f"{k}={urllib.parse.quote_plus(str(v))}" for k, v in sorted_params])
    # Tạo chuỗi hash
    hash_data = '&'.join([f"{k}={v}" for k, v in sorted_params])
    vnp_SecureHash = hmac.new(vnp_HashSecret.encode(), hash_data.encode(), hashlib.sha512).hexdigest()
    payment_url = f"{vnp_Url}?{query_string}&vnp_SecureHash={vnp_SecureHash}"
    return payment_url

def verify_vnpay_response(params, secure_hash):
    vnp_HashSecret = settings.VNPAY_HASH_SECRET
    params = {k: v for k, v in params.items() if k != 'vnp_SecureHash' and k != 'vnp_SecureHashType'}
    sorted_params = sorted(params.items())
    hash_data = '&'.join([f"{k}={v}" for k, v in sorted_params])
    check_hash = hmac.new(vnp_HashSecret.encode(), hash_data.encode(), hashlib.sha512).hexdigest()
    return check_hash == secure_hash 