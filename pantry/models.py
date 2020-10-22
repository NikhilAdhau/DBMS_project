from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    p_id = models.AutoField(primary_key = True)
    p_name = models.CharField(max_length=30)
    category = models.CharField(max_length=300, default='')
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to='pantry/images', default='')
    p_quantity = models.IntegerField(default = 0)
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
    def __str__(self):
        return self.cart_id

class Cart_item(models.Model):
    cart_id = models.ForeignKey('Cart', on_delete = models.CASCADE, default=None)
    p_id = models.ForeignKey('Product', on_delete = models.CASCADE, default=None)
    prod_quantity = models.IntegerField(default=1)


class Order(models.Model):
    order_id = models.AutoField(primary_key = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, default=None)

class Order_item(models.Model):
    order_id = models.ForeignKey('Order', on_delete = models.CASCADE, default=None)
    p_id = models.ForeignKey('Product', on_delete = models.CASCADE, default=None)
    date = models.DateTimeField()
    shipped = models.BooleanField()
    deliverred = models.BooleanField()
    cancelled = models.BooleanField()

class Order_quantity(models.Model):
    p_id = models.ForeignKey('Product', on_delete = models.CASCADE, default=None)
    quantity = models.IntegerField()

class Wishlist(models.Model):
    wishlist_id = models.AutoField(primary_key = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, default=None)

class Wishlist_item(models.Model):
    wishlist_id = models.ForeignKey('Wishlist', on_delete = models.CASCADE, default=None)
    p_id = models.ForeignKey('Product', on_delete = models.CASCADE, default=None)