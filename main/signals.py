from django.db.models.signals import post_save
from django.dispatch import receiver
from main.models import Cart,Wishlist

def total_update(Class):
    @receiver(post_save, sender=Class)
    def update(sender, instance, created, **kwargs):
    
        new_total = instance.compute_total_amount()

        if instance.total_amount != new_total:
            Class.objects.filter(id=instance.id).update(total_amount=new_total)

total_update(Cart)

total_update(Wishlist)

