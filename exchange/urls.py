from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.log),
    path('register', views.register),
    path('trade_buy', views.new_order_buy),
    path('trade_sell', views.new_order_sell),
    path('order_active', views.order_active),
    path('order_inactive', views.order_inactive)
]