from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from main.models import *
from api.serializers import ProductSerializer,CartSerializer
from django.db.models import Q
from e_auth.utils import send_otp 
from e_auth.models import Customer , Address

# Create your views here.
@api_view
@permission_classes([IsAuthenticated])
def get(request):
    products = Product.objects.all()
    

    serializers = ProductSerializer(products,many=True)
    return Response(serializers.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_remove_cart(request):

    product_id = request.data.get('product_id')
    product = get_object_or_404(Product, id=product_id)

    quantity = int(request.data.get('quantity', 1))

    cart_item = Cart.objects.filter(
        product=product,
        user=request.user
    ).first()

    if cart_item:
        cart_item.delete()
        cart_count = Cart.objects.filter(user=request.user).count()
        return Response({
            "status": "Removed",
            "product_id": str(product_id),
            "cart_count": cart_count
        })

    cart_item = Cart.objects.create(
        product=product,
        user=request.user,
        quantity=quantity
    )

    cart_count = Cart.objects.filter(user=request.user).count()

    return Response({
        "status": "Added",
        "product_id": str(product_id),
        "cart_count": cart_count
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_cart_quantity(request):

    cart_id = request.data.get('cart_id')
    quantity = int(request.data.get('quantity',1))

    cart = get_object_or_404(Cart,id=cart_id)
    cart.quantity = quantity
    cart.save()
    new_total = request.user.cart_user.aggregate(
        total = Sum("total_amount")
    )['total'] or 0
    return Response({   
        "status": "success",
        "product_name": cart.product.name,
        "new_total" : new_total
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_shipping(request):  
    shipping_id = request.data.get('shipping_id')
    order_id = request.data.get('order_id')

    order = get_object_or_404(Order,id=order_id)
    shipping = get_object_or_404(ShippingOption,id=shipping_id)
    
    items_total = sum(item.get_total() for item in order.ordering.all())
    new_total = items_total + shipping.price
    
    order.shipping_price = shipping
    order.total_amount = round(new_total,2)
    order.save()    
    
    return Response({
        'total_amount': order.total_amount,
        'shipping_type': shipping.shipping_type,
        'shipping_price':shipping.price,
        
    })

@api_view(['POST'])    
@permission_classes([IsAuthenticated])
def update_order_address(request):
    address_id = request.data.get('address_id')
    order_id = request.data.get('order_id')

    address = Address.objects.get(id=address_id)
    order = get_object_or_404(Order,id=order_id)
    order.address = address
    order.save()
    return Response({
        'type': address.address_type
    })

@api_view(['POST'])
def reset_otp(request):
    email = request.data.get('email')
    send_otp(email)
    return Response({
        'status':"Resent OTP sucessfully"
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_profile_shipping(request):
    shipping_id = request.data.get('shipping_id')
    shipping = get_object_or_404(ShippingOption,id=shipping_id)
    customer = Customer.objects.get(profile__user = request.user)
    customer.shipping = shipping
    customer.save()
    type = shipping.shipping_type
    return Response({
        'status':"success",
        "type": type.capitalize()
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_profile_address(request):
    address_id = request.data.get('address_id')
    address = get_object_or_404(Address,id=address_id)
    address.is_default = True
    address.save()
    customer = request.user.profile.first()
    customer.address = address
    customer.save()

    return Response({
        'status': "success",
        'address': address.address_type.capitalize()
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_order(request):
    order_id = request.data.get('order_id')
    order = get_object_or_404(Order,id = order_id)
    order.status = "CANCELLED"
    order.save()
    return Response({
        'status': 'success'
    })
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_order(request):
    order_id = request.data.get('order_id')
    order = get_object_or_404(Order,id = order_id)
    if order.status == "PAID" or order.status == "DELEVIRED" :
        order.status = "DELETED"
        order.save()
    order.delete()
    return Response({
        'status': 'success'
    })