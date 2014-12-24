from django.contrib import admin
from core.models import *

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(ProjectProfile)
admin.site.register(PriceUnit)
admin.site.register(ShopCartItem)
admin.site.register(ShippingAddress)
admin.site.register(Order)
