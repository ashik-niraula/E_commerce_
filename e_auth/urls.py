from e_auth import views
from django.urls import path

urlpatterns = [
    path('up/',views.signup_page,name='signup'),

    path('up/verify-otp',views.verify_otp,name='otpverify'),

    path('in/',views.login_page,name='login'),

    path('out/',views.logout_page,name='logout'),

    path('address-info/',views.user_detail_page,name='add_address'),
    path('edit-address/<pk>/',views.edit_address,name='edit_address'),

    path('profile/<username>',views.user_profie,name='user_profile'),

    path('orders/',views.user_orders,name='user_orders'),

    path('order-detail/<order_id>',views.user_order_detail,name='order_detail'),

    
]
