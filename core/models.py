from django.db import models
from multiselectfield import MultiSelectField
from django.conf import settings
from django_countries.fields import CountryField
# Create your models here.
# variables 
COLOR=(
        ('#800080','PURPLE'),
        ('#ff0000','RED'),
        ('#008000','GREEN'),
        ('#000000','BLACK'),
        ('#f2f2f2','WHITE')

    )

SIZE=(
        ('S','SMALL'),
        ('M','MEDIUM'),
        ('L','LARGE'),
        ('XL','XLARGE')
    )

class Item(models.Model):
  

    title=models.CharField(max_length=50)
    price=models.IntegerField()
    previous_price=models.IntegerField(blank=True,null=True)
    description=models.TextField()
    image_core=models.ImageField(default=False)
    color_core_default=models.CharField(max_length=100,choices=COLOR)
    size_core_default=models.CharField(max_length=100,choices=SIZE)
    color_disponnible=MultiSelectField(max_length=100,choices=COLOR)
    size_disponnible=MultiSelectField(max_length=10,choices=SIZE)

    objects=models.Manager()
    def __str__(self):
        return self.title


class Imagedetail(models.Model):
    item=models.ForeignKey(Item,on_delete=models.CASCADE,blank=True,null=True)
    image=models.ImageField(default=False)
    color_secondary=models.CharField(max_length=100,choices=COLOR)
    
    
    objects=models.Manager()


class OrderItem(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    item=models.ForeignKey(Item,on_delete=models.CASCADE)
    size=models.CharField(max_length=10,default=True)
    color=models.CharField(max_length=100,default=True)
    quantity=models.IntegerField(default=1)
    is_ordered=models.BooleanField(default=False)


    objects=models.Manager()
    def __str__(self):
        return self.item.title
    
    def get_total(self):
        return self.quantity * self.item.price

    


class Order(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    order_items=models.ManyToManyField(OrderItem)
    is_ordered=models.BooleanField(default=False)
    date_creation=models.DateTimeField()
    coupon=models.ManyToManyField('Coupon')
    adress=models.OneToOneField('BillingAdress',on_delete=models.SET_NULL,blank=True,null=True)
    payment=models.ForeignKey('Payment',on_delete=models.SET_NULL,blank=True,null=True)
  


    def __str__(self):
        return self.user.username

    def get_subtotal(self):
        subtotal=0
        for item in self.order_items.all():
            subtotal+=item.get_total()
        return subtotal

    def get_total(self):
        total=self.get_subtotal()
        for coupon in self.coupon.all():
            total-=coupon.amount
        return total
            


class Coupon(models.Model):
    coupon=models.CharField(max_length=10)
    amount=models.IntegerField()
    expiration=models.BooleanField(default=False)
    minimal_amount_required=models.IntegerField()
    
    def __str__(self):
        return self.coupon
    


class BillingAdress(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,blank=True,null=True)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    adress1=models.CharField(max_length=200)
    adress2=models.CharField(max_length=200,default=None)
    city=models.CharField(max_length=50)
    zip=models.IntegerField()
    phone=models.IntegerField()
    country=CountryField(multiple=False)
    

class Payment(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,blank=True,null=True)
    stripe_id_charge=models.CharField(max_length=30)
    amount=models.FloatField()
    date_payment=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username 
    