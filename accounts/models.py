from re import T
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    mobile = models.CharField(max_length=20)
    otp = models.CharField(max_length=6,default=0000,null=True,blank=True)
    name = models.CharField(max_length=100,null=True,blank=True)
    gender=models.CharField(max_length=10,null=True,blank=True)
    city=models.CharField(max_length=100,null=True,blank=True)
    state=models.CharField(max_length=100,null=True,blank=True)
   



    def __str__(self):
        return self.name


    