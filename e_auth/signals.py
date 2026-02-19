from django.contrib.auth.models import User
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from e_auth.models import Customer , Vendor , Profile,Address
from main.models import Cart , Order , Wishlist

@receiver(post_save,sender=Profile)
def create_profile(sender,instance,created,**kwargs):
    if created:
        if instance.is_customer == True:
            Customer.objects.create(profile=instance)
        if instance.is_vendor == True:
            Vendor.objects.create(profile=instance)




@receiver([post_save,post_delete] , sender = Order )        
def update_count(sender,instance,*args, **kwargs):
    profile =  instance.user.profile.first()
    profile.customer.update_orders()   

@receiver([post_save,post_delete] , sender = Wishlist )        
def update_count(sender,instance,*args, **kwargs):
    profile =  instance.user.profile.first()
    profile.customer.update_wishlist()    
    
@receiver([post_save,post_delete] , sender = Order )        
def update_count(sender,instance,*args, **kwargs):
    profile =  instance.user.profile.first()
    profile.customer.update_total_spent()    



                    