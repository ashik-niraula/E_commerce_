from django.db.models import Q
import uuid
from django.core.mail import send_mail
import shortuuid
from django_esewa import  EsewaPayment,generate_signature
import datetime
import paypalrestsdk
def Search(request,products):
    search = request.GET.get("search")
    category = request.GET.get("category")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")

    if search:
        products = products.filter(
            Q(category__name__icontains=search) |
            Q(name__icontains=search) |
            Q(description__icontains=search) |
            Q(seller__username__icontains=search)
        )
    if category:
        products = products.filter(category__name__icontains=category)    

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)
    return products

def esewa_payment(order):
    total = (order.total_amount * 145)
    amount = sum(item.get_total() for item in order.ordering.all()) * 145
    payment = EsewaPayment(
            product_code="EPAYTEST",
            success_url="http://127.0.0.1:8000/payment-success/",
            failure_url=f"http://127.0.0.1:8000/payment-failed/?order_id={order.id}",
            amount= amount,
            tax_amount=0.00,
            total_amount= total,
            product_delivery_charge=0.00,
            product_service_charge=0.00,
            transaction_uuid=uuid.uuid4(),
            secret_key="8gBm/:&EnhH.1/q",
            )
    signature = payment.create_signature()
    return payment

def paypal_payment(order):
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://127.0.0.1:8000/payment-success/",
            "cancel_url": f"http://127.0.0.1:8000/payment-failed/?order_id={order.id}",
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "RadhaPiyaShop",
                    "sku": f"{order.id}",
                    "price": "000",
                    "currency": "USD",
                    "quantity": 1,
                }]
            },
            "amount": {
                "total": f"{order.total_amount}",
                "currency": "USD",
            },
            "description": "Test payment",
        }]
    })   
    return payment

    

def send_payment_success_email(request,order,):
    subject = f"Payment Successful - Order #{order.order_num}"
    recipient = [request.user.email]

    message = f"""
    Hi {request.user.get_full_name()},

    Thank you for your purchase! Your payment has been successfully processed and your order is confirmed.

    Order Confirmation
    -------------------
    Order Number: {order.order_num}
    Order Date: {order.paid_at.strftime('%B %d, %Y %H:%M')}
    Invoice Number: {order.invoice}
    Payment Method: {order.get_payment_method_display()}
    Payment ID: {order.payment_id}
    Total Amount: ${order.total_amount}

    Shipping Address
    ----------------
    {order.address.address}
    {order.address.state}

    Estimated Delivery: {order.shipping_price.get_shipping_type_display()}

    Need Help?
    ----------
    If you have questions or need assistance with your order, please contact our support team:
    - Email: support@RadhaPiya.com
    - Call: 1-800-123-4567

    Thank you for shopping with us!

    Best regards,
    RadhaPiyaStore Team
    """

    send_mail(
        subject=subject,
        message=message,
        from_email="noreply@RadhaPiya.com",
        recipient_list=recipient,
        fail_silently=False,
    )


     
            
