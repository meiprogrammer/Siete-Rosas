from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class Products (models.Model):
    name = models.CharField(max_length=34)
    colors = models.JSONField(default=list)
    price = models.IntegerField(default=20)
    id = models.AutoField(primary_key=True)

class Events (models.Model):
    name = models.CharField(max_length=64)
    location = models.CharField(max_length=128)
    description = models.CharField(max_length=128)

class Pay (models.Model):
    user = models.CharField(max_length=50)
    state = models.CharField(max_length=16)
    city = models.CharField(max_length=36)
    cep = models.IntegerField()
    number = models.IntegerField()
    complement = models.CharField(max_length=50)
    id = models.AutoField(primary_key=True)
    product = models.IntegerField()
    status = models.CharField(max_length=7)
    merchant_order_id = models.TextField(default=0)