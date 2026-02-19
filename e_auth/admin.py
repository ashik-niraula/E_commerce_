from django.contrib import admin
from e_auth.models import Profile,Vendor,Customer,Address
# Register your models here.
class VenderAdmin(admin.ModelAdmin):
    list_display = ('profile','shop_name','status','total_orders')
    list_filter = ('profile','status','total_orders')

admin.site.register(Profile)
admin.site.register(Vendor,VenderAdmin)
admin.site.register(Customer)
admin.site.register(Address)

