'''
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('payment',views.payment,name='payment'),
    path('proceed-to-pay',views.razorpaycheck,name='proceed-to-pay'),

]
'''