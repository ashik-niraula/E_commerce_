from django.urls import path,include
from api import views
urlpatterns = [
    path('products/',views.get),
    path('cart/',views.add_remove_cart),
    path('update-cart-quantity/',views.update_cart_quantity),
    path("update-shipping/", views.update_shipping, name="update_shipping"),

    path("update-order-address/", views.update_order_address),

    path("resent-otp/", views.reset_otp, name="resendotp"),
    path("update-profile-shipping/", views.update_profile_shipping, name="update_shipping"),
    path("update-profile-address/", views.update_profile_address, name="update_address"),

    path("cancel-order/", views.cancel_order, name="cancel_order"),

    path("delete-order/", views.delete_order),
    
]   
