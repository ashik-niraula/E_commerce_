from django.contrib import admin
from main.models import *
# Register your models here.
admin.site.register(Category)
admin.site.register(ShippingOption)
admin.site.register( HomeSlider)
admin.site.register( Order)
admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(Cart)
# admin.site.register(Cheakout)