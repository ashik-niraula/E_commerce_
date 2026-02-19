from django.urls import path , include
from main import views
urlpatterns = [
    path('',views.home_page,name='home'),
    path('home/',views.home_page,name='home'),

    path('products/',views.product_page,name='products'),
    path('product-detail/<slug:slug>/',views.product_detail_page,name='product_detail'),

    path('cart/',views.cart_page,name='cart'),

    path('buynow/<slug>',views.buynow,name='buynow'),
    
    path('cheakout/<uuid:order_id>',views.cheakout_page,name='cheakout'),

    path('payment/<uuid:id>',views.payment_page,name='payment'),
    path('payment-success/',views.payment_success,name='paysuccess'),
    path('payment-failed/',views.payment_failed,name='payfailed'),
    
    path('vendor_profile/',views.vendor_page,name='vendor'),
    
    

]
