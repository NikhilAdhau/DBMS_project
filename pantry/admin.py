from django.contrib import admin
from .models import Product
from .models import Product_category
from .models import Cart
from .models import Cart_item
from .models import Order
from .models import Order_item
from .models import Order_quantity
from .models import Wishlist
from .models import Wishlist_item
from .models import Profile


admin.site.register(Product)
admin.site.register(Product_category)
admin.site.register(Cart)
admin.site.register(Cart_item)
admin.site.register(Order)
admin.site.register(Order_item)
admin.site.register(Order_quantity)
admin.site.register(Wishlist)
admin.site.register(Wishlist_item)
admin.site.register(Profile)
