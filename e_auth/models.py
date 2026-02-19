from django.db import models
from django.db.models import Sum
from shortuuid.django_fields import ShortUUIDField
import shortuuid
from django.contrib.auth.models import User,AbstractUser
from cloudinary.models import CloudinaryField
from django.core.validators import MaxValueValidator
from main.models import ShippingOption , Order , Wishlist , Cart

class Profile(models.Model):
    pid = ShortUUIDField(unique=True,length=10,max_length=20,prefix="pro", alphabet="abcdefghij12345")
    user = models.ForeignKey(User,related_name='profile', on_delete=models.CASCADE)
    bio = models.TextField(blank=True,null=True)
    image = CloudinaryField('profile_image',default="static/css/icon.jpeg",null=True,folder="D_commerce/profile")
    cover_image = CloudinaryField('cover_image',blank=True,null=True,folder="D_commerce/profile/cover")
    is_vendor = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)
    created_at = models.DateTimeField( auto_now_add=True)
    phonenumber = models.CharField(max_length=100, null=True)

    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)
        

    def __str__(self):
        return self.user.get_full_name() or self.user.username
    

class Address(models.Model):

    ADDRESS_TYPE = (
        ('home', 'Home'),
        ('office', 'Office'),
        ('temporary', 'Temporary'),
    )

    country = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100)
    landmark = models.CharField(max_length=100, null=True, blank=True)
    
    address_type = models.CharField(choices=ADDRESS_TYPE,null=True, max_length=50)

    is_default = models.BooleanField(default=False)
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE,null=True,related_name='user_address',)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.is_default:
            Address.objects.filter(
                profile=self.profile
            ).exclude(id=self.id).update(is_default=False)

class Vendor(models.Model):
    STATUS = (
        ('PENDING','Pending'),
        ('APPROVED','Approved')
    )

    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="vendor")
    shop_name = models.CharField(max_length=200,null=True)
    pan = models.CharField(max_length=50,null=True)
    total_orders = models.PositiveIntegerField(default=0)
    rating = models.FloatField(default=0)
    status = models.CharField(choices=STATUS,default='PENDING', max_length=50)
    chat_resp_time = models.PositiveIntegerField(validators=[MaxValueValidator(100)], default="100")
    shipping_on_time = models.PositiveIntegerField(validators=[MaxValueValidator(100)], default="100")
    authentic_rating = models.PositiveIntegerField(validators=[MaxValueValidator(100)], default="100")

    def __str__(self):
        return f"Seller: {self.profile.user.username}"

class Customer(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="customer")
    total_spent = models.DecimalField( default=0.00,max_digits=10, decimal_places=2)
    shipping = models.ForeignKey(ShippingOption,null=True, on_delete=models.CASCADE)
    orders = models.IntegerField(default=0)
    wishlists = models.IntegerField(default=0)
    following_sellers = models.ManyToManyField(Vendor,related_name='following', blank=True)

    def update_orders(self):
        self.orders = Order.objects.filter(user=self.profile.user,status="PAID").count()
        self.save(update_fields=['orders'])

    def update_wishlist(self):
        self.wishlists = Wishlist.objects.filter(user=self.profile.user).count()  
        self.save(update_fields=['wishlists'])  

    def update_total_spent(self):
        self.total_spent = Order.objects.filter(user=self.profile.user,status='PAID').aggregate(total=Sum('total_amount')) ['total'] or 0    
        self.save(update_fields=['total_spent'])

    def __str__(self):
        return f"Buyer:{self.profile.user.username}"
    


