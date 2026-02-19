from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse
from django.http import HttpResponseBadRequest,HttpResponse
from django.db.models import Q
from .models import *
from main.utils import Search,esewa_payment,paypal_payment , send_payment_success_email
from django_esewa import  EsewaPayment,generate_signature , verify_signature 
import datetime 
import base64
import json
import shortuuid
import paypalrestsdk
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from e_auth.models import Profile , Address
import random

# Create your views here.

def home_page(request):

    featured = Product.objects.filter(is_featured = True).select_related('category','seller')
    sliders = HomeSlider.objects.filter(is_active=True)
    categories = Category.objects.filter(trending = True)
    
    user_cart = None
    if request.user.is_authenticated:
        user_cart = request.user.cart_user.values_list('product_id',flat=True)
        profile, created = Profile.objects.get_or_create(user=request.user)
    
    context = {
        'featured': featured,
        'sliders':sliders,
        "user_cart": user_cart ,
        'categories': categories,
    }    

    return render(request,"main/index.html",context)

def vendor_page(request)   :
    return render(request,'main/index2.html') 

@login_required(login_url="login")
def product_page(request):
    products = Product.objects.all()
    categories = Category.objects.only('id', 'name')
    user_cart = request.user.cart_user.values_list('product_id',flat=True)
    
    products = Search(request,products)
    
    context = {
        "products": products,
        'categories':categories,
        "user_cart":user_cart
    }

    return render(request, "main/products.html", context)

@login_required(login_url="login")
def product_detail_page(request,slug):
    product = get_object_or_404(Product,slug=slug)
    related = Product.objects.filter(category=product.category).exclude(id = product.id)
    user_cart = request.user.cart_user.values_list('product_id',flat=True)

    quantity = 1
    if product.id in user_cart:
        quantity = request.user.cart_user.get(product=product).quantity
    
    context = {
        'product':product,
        'related': related,
        "user_cart": user_cart,
        "quantity":quantity
    }

    return render(request,'main/product_detail.html',context)    

@login_required(login_url="login")
def cart_page(request):
    carts = request.user.cart_user.all().select_related('product')
    
    user_cart = request.user.cart_user.values_list('product_id',flat=True)

    total_amount = request.user.cart_user.aggregate(
        total = Sum('total_amount')
    )['total'] or 0
    
    context = {
        "carts":carts,
        "user_cart": user_cart,
        "total_amount": round(total_amount,2),
    }
    if request.method == "POST":
        profile = request.user.profile.first()
        if not Address.objects.filter(profile=profile).exists():
            return redirect('add_address')
        order  = Order.objects.create(
            user = request.user,
            total_amount = total_amount
        )
        
        for item in request.user.cart_user.all() :
            OrderItem.objects.create(
                order = order,
                product = item.product,
                price = item.product.price,
                quantity = item.quantity
            )
        carts.delete()    
        return redirect('cheakout',order.id)        

    return render(request,'main/cart.html',context) 

@login_required(login_url="login")
def buynow(request,slug):
    profile = request.user.profile.first()
    if not Address.objects.filter(profile=profile).exists():
        return redirect('add_address')
    product = get_object_or_404(Product,slug=slug)
    quantity = int(request.POST.get('quantity',1))
    
    total_amount = product.price * quantity

    
    order,created = Order.objects.get_or_create(
        user=request.user,   
        total_amount = total_amount,
        status = "PENDING",
        slug = slug,
    )
    if created:
        order_item = OrderItem.objects.create(
        order = order, 
        product = product,
        price = product.price,
        quantity = quantity
        )
    
    return redirect('cheakout',order.id)

@login_required(login_url="login")
def cheakout_page(request,order_id):
    order = get_object_or_404(Order,id=order_id)
    orderitems = OrderItem.objects.filter(order=order)

    if order.payment_method and order.paid_at and order.order_num:
        new_order = Order.objects.create(
            user = request.user,
            total_amount = order.total_amount,
            status = "PENDING"
        )
        order = new_order
        for item in orderitems :
                OrderItem.objects.create(
                    order = order,
                    product = item.product,
                    price = item.product.price,
                    quantity = item.quantity
                )
    profile = request.user.profile.first()            
    shipping = profile.customer.shipping
    if shipping is not None:
        order.shipping_price = shipping
    else:    
        order.shipping_price = ShippingOption.objects.all().first()

    default_address = Address.objects.get(profile=profile)
    if default_address.is_default == "True":
        order.address = default_address
    else:    
        order.address = profile.user_address.all().first()
    order.save()
    addresses = profile.user_address.all()
    shipping = ShippingOption.objects.all()
    
    context = {
        'order': order,
        'orderitems':orderitems,
        'shipping': shipping,
        'sub_total': sum(item.get_total() for item in order.ordering.all()),
        'addresses': addresses ,
        'profile': profile
    }
    
    return render(request,'main/cheakout.html',context) 

@login_required(login_url="login")
def payment_page(request,id):
    order = get_object_or_404(Order,id=id)
    orderitem = OrderItem.objects.filter(order=order)

    if request.method == "POST":
        method = request.POST.get('method')

        if method == 'esewa':
            payment = esewa_payment(order)
            order.transaction_id = payment.transaction_uuid
            order.save()
            return render(request,"main/payments/esewa.html",{ 'form':payment.generate_form()})
        
        elif method == 'paypal':
            payment = paypal_payment(order)
            if payment.create():
                for link in payment.links:
                    if link.rel == "approval_url":
                        order.paid_at = datetime.datetime.now()
                        order.transaction_id = uuid.uuid4() 
                        order.payment_id = payment.id
                        order.order_num = f'ORD-{random.randint(10000, 999999)}'
                        order.invoice = shortuuid.uuid()[:10]
                        order.save()
                        return redirect(link.href)
            else:
                return HttpResponse("Error creating PayPal payment")
        else:
            messages.info(request, "Select the Payment Option.")

            return redirect('payment',id)    
            
    context = {
        "order":order,
        "orderitem": orderitem,
        'sub_total': sum(item.get_total() for item in order.ordering.all()),
        
    }

    return render(request,'main/payment.html',context) 

@login_required(login_url="login")
def payment_success(request):
    data = request.GET.get('data')
    if data:
        is_valid,signature = verify_signature(data)
        if is_valid:
            trans_id = signature.get('transaction_uuid')
            order = get_object_or_404(Order,transaction_id=trans_id)
            order.status = "PAID"
            order.payment_method ="ESEWA"
            if not order.order_num:
                order.order_num = f'ORD-{random.randint(10000, 999999)}'
                order.paid_at = datetime.datetime.now()
                order.invoice = shortuuid.uuid()[:10]
            order.payment_id = signature.get('transaction_code')
            order.save()
            if not order.email_sent:
                send_payment_success_email(request,order)
                order.email_sent = True
                order.save()

    payment_id = request.GET.get('paymentId')
    token = request.GET.get('token')
    payer_id = request.GET.get('PayerID')
    if payment_id:
        payment = paypalrestsdk.Payment.find(payment_id)
        if payment:
            order = get_object_or_404(Order,payment_id=payment_id)
            order.transaction_id = token
            order.payer_id = payer_id
            order.status = "PAID"
            order.payment_method = "PAYPAL"
            order.save()
            if not order.email_sent:
                send_payment_success_email(request,order)
                order.email_sent = True
                order.save()

    if  order.payment_id and order.status == "PAID":
        return render(request,'main/payment_success.html',{"order":order})    
    else:
        return redirect('home')    
            
    
@login_required(login_url="login")
def payment_failed(request):
    order_id = request.GET.get('order_id')
    order = get_object_or_404(Order,id = order_id)
    order.status = "cancelled"
    order.save()
    return render(request,'main/payment_failed.html',{'order_id':order_id})  
   

