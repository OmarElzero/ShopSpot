from django.db import models
from django.contrib.auth.models import User
from django.apps import AppConfig

import categories.models
# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.BigIntegerField(null=True)
    email = models.EmailField(max_length=50)
    address = models.TextField()
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username



