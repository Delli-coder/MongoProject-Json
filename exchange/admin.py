from django.contrib import admin
from .models import Profile, OrderSell, OrderBuy

admin.site.register(Profile)
admin.site.register(OrderSell)
admin.site.register(OrderBuy)

# Register your models here.
