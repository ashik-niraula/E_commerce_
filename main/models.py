from django.db import models
import uuid
from cloudinary.models import CloudinaryField
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models import Sum
import shortuuid
from shortuuid.django_fields import ShortUUIDField
# from e_auth.models import Vendor,Costomer

# Create your models here.
class Category(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(unique=True, max_length=50)
    title = models.CharField(blank=True,null=True, max_length=50)
    slug = models.SlugField(unique=True,blank=True)
    trending = models.BooleanField(default=False)
    category_image = CloudinaryField('category_image',folder='Ecommerce/Image/Category')
   
    @property   
    def get_image_url(self):
        return self.category_image.build_url(
        width=400,
        crop="fill",
        quality="auto",
        fetch_format="auto"
        )
    
    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    
    def save(self,*args, **kwargs)  :
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{shortuuid.uuid}"
            self.slug = slug  
        super().save(*args, **kwargs)      

class HomeSlider(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)        
    slider_image = CloudinaryField('Slider',folder='Ecommerce/Image/Slider')
    title = models.CharField( max_length=500)
    sub_title =  models.CharField( max_length=50,blank=True,null=True)
    category = models.ForeignKey(Category,related_name='slider_cate', on_delete=models.CASCADE)

    is_active = models.BooleanField(default=False)

    @property   
    def get_image_url(self):
        return self.slider_image.build_url(
        width=400,
        crop="fill",
        quality="auto",
        fetch_format="auto"
        )

    def __str__(self):
        return f"{self.category.name}----{self.sub_title}"
    
class Product(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    product_image = CloudinaryField('Product',folder='Ecommerce/Image/Product')
    name = models.CharField(max_length=150)
    pip = models.CharField( max_length=6,blank=True,null=True)
    description = models.TextField()
   
    price = models.DecimalField(max_digits=10, decimal_places=2)
    previous_price = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
    stock = models.PositiveIntegerField()
    category = models.ForeignKey(Category,related_name='product_cate', on_delete=models.CASCADE)
    seller = models.ForeignKey(User,related_name="seller", on_delete=models.CASCADE)
    is_avilable = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    rating = models.PositiveIntegerField(blank=True,null=True)
    slug = models.SlugField(unique=True,blank=True)
    
    def get_discount(self):
        if self.previous_price > self.price:
            discount = (self.previous_price - self.price)/self.previous_price * 100
            discount = round(discount,0)
            return discount
     
    @property   
    def get_image_url(self):
        return self.product_image.build_url(
        width=400,
        crop="fill",
        quality="auto",
        fetch_format="auto"
        )

    def save(self,*args, **kwargs)  :
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{shortuuid.uuid()}"
            self.slug = slug  
        super().save(*args, **kwargs)  

    def __str__(self):
        return f"{self.name} of Category {self.category.name} of User {self.seller.get_full_name()}"
    
class ShippingOption(models.Model):
    """Simple shipping options with fixed prices"""
    SHIPPING_TYPES = [
        ('standard', 'Standard Shipping (3-7 days)'),
        ('express', 'Express Shipping (1-3 days)'),
        ('overnight', 'Overnight Shipping (next day)'),
    ]
    shipping_type = models.CharField(max_length=20, choices=SHIPPING_TYPES ,default='standard')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    def __str__(self):
        return f"{self.shipping_type}--{self.price}"


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    product = models.ForeignKey(Product , related_name='cart_products', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart_user")

    quantity = models.PositiveIntegerField(default=1)

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def compute_total_amount(self):
        product_amount = self.product.price * self.quantity
        return product_amount 
        

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

    
class Order(models.Model):
    STATUS = (
        ("PENDING", "Pending"),
        ("PAID", "Paid"),
        ("SHIPPED", "Shipped"),
        ("CANCELLED", "Cancelled"),
        ("DELETED", "Deteled"),
    )

    PAYMENT_METHODS = (
        ("COD", "Cash On Delivery"),
        ("KHALTI", "Khalti"),
        ("ESEWA", "eSewa"),
        ("PAYPAL", "paypal"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, related_name="orders", on_delete=models.SET_NULL, null=True)

    status = models.CharField(max_length=20, choices=STATUS, default="PENDING")

    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, blank=True, null=True)
    payment_id = models.CharField(max_length=500, blank=True, null=True)
    payer_id = models.CharField(max_length=500, blank=True, null=True)

    transaction_id = models.CharField(max_length=150, blank=True, null=True)
    invoice = ShortUUIDField(blank=True,null=True,prefix="INV",max_length=13,length=10)
    
    slug = models.SlugField(blank=True,null=True)
    shipping_price = models.ForeignKey(
        ShippingOption, null=True, blank=True, on_delete=models.SET_NULL
    )
    address = models.ForeignKey("e_auth.Address", related_name='order_address',null=True, on_delete=models.CASCADE)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
    order_num = models.CharField(max_length=10,blank=True,null=True)
    email_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Order {self.status} - {self.user} - {self.ordering.first()} and more"
 
class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    order = models.ForeignKey(Order,related_name='ordering' , on_delete=models.CASCADE)
    product = models.ForeignKey(Product,related_name="product_ordering", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)

    quantity = models.PositiveIntegerField(default=1)
    
    def get_total(self):
        return (self.price*self.quantity)
    
    def __str__(self):
        return f'{self.product.name} * {self.quantity}'
    

class Wishlist(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    product = models.ForeignKey(Product, related_name='wishlist_products', on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name='wishlist_user', on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=1)

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    shipping_price = models.ForeignKey(
        ShippingOption,
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    def update_total_amount(self):
        product_amount = self.product.price * self.quantity
        shipping_cost = self.shipping_price.price if self.shipping_price else 0
        self.total_amount = product_amount + shipping_cost
        self.save(update_fields=['total_amount'])

    def __str__(self):
        return f"{self.user.username} wishlisted {self.product.name}"
    
        
