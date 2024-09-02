from django.db import models
from django.contrib.auth.models import User
from django.apps import AppConfig
from django.db import models
from django.utils.crypto import get_random_string

import categories.models
# Create your models here.


class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    phone = models.BigIntegerField(null=True)
    email = models.EmailField(max_length=50, unique=True)
    address = models.TextField()
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.username

class CustomerToken(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='auth_token')
    key = models.CharField(max_length=40, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = get_random_string(40)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.key



