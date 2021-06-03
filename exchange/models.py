from django.db import models
from django.contrib.auth.models import User
from djongo.models.fields import ObjectIdField


class Profile(models.Model):
    _id = ObjectIdField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ips = models.Field(default=[])
    subprofiles = models.Field(default={})
    btc_wallet = models.FloatField()
    original_btc = models.FloatField()
    wallet = models.FloatField()


class OrderBuy(models.Model):
    _id = ObjectIdField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    price = models.FloatField()
    original_quantity = models.FloatField()
    quantity = models.FloatField()
    active = models.Field(default='True')


class OrderSell(models.Model):
    _id = ObjectIdField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    price = models.FloatField()
    original_quantity = models.FloatField()
    quantity = models.FloatField()
    active = models.Field(default='True')


# Create your models here.
