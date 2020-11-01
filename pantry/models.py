from django.db import models
from django.contrib.auth.models import User
import datetime
import django

class Product(models.Model):
    p_id = models.AutoField(primary_key = True)
    p_name = models.CharField(max_length=30)
    category = models.CharField(max_length=300, default='')
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to='pantry/images', default='')
    availability = models.BooleanField(default=True)
    def __str__(self):
        return self.p_name

class Product_category(models.Model):
    category = models.ForeignKey('Product', on_delete = models.CASCADE, default=None)
    subcategory = models.CharField(max_length=300, default = '')

class Cart(models.Model):
    cart_id = models.AutoField(primary_key = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, default=None)
    total_cost = models.IntegerField(default = 0)

class Cart_item(models.Model):
    cart_id = models.ForeignKey('Cart', on_delete = models.CASCADE, default=None)
    p_id = models.ForeignKey('Product', on_delete = models.CASCADE, default=None)
    prod_quantity = models.IntegerField(default = 0)

class Order(models.Model):
    order_id = models.AutoField(primary_key = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, default=None)
    order_success = models.BooleanField(default=False)
    date = models.DateTimeField(default=django.utils.timezone.now)
    order_amount = models.IntegerField(default = 0)
    order_address = models.CharField(max_length = 500, default = '')
    order_city = models.CharField(max_length = 50, default = '')
    order_state = models.CharField(max_length = 50, default = '')
    order_phone = models.BigIntegerField(default = 0000000000)



class Order_item(models.Model):
    order_id = models.ForeignKey('Order', on_delete = models.CASCADE, default=None)
    p_id = models.ForeignKey('Product', on_delete = models.CASCADE, default=None)
    shipped = models.BooleanField(default=False)
    deliverred = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)

class Order_quantity(models.Model):
    order_id = models.ForeignKey('Order', on_delete = models.CASCADE, default=None)
    p_id = models.ForeignKey('Product', on_delete = models.CASCADE, default=None)
    quantity = models.IntegerField(default=1)

class Wishlist(models.Model):
    wishlist_id = models.AutoField(primary_key = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, default=None)

class Wishlist_item(models.Model):
    wishlist_id = models.ForeignKey('Wishlist', on_delete = models.CASCADE, default=None)
    p_id = models.ForeignKey('Product', on_delete = models.CASCADE, default=None)
