from django.db import models
from django.contrib.auth.models import User
from django.apps import AppConfig
from django.db import models
from django.utils.crypto import get_random_string
from django.core.exceptions import ValidationError

import categories.models
# Create your models here.


class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, editable=False)
    name = models.CharField(max_length=100)
    phone = models.BigIntegerField(null=True)
    email = models.EmailField(max_length=50, unique=True)
    address = models.TextField()
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)


    def clean(self):
        if self.phone and len(str(self.phone)) < 10:  # Assuming phone should be at least 10 digits
            raise ValidationError("Phone number must be at least 10 digits long.")
        super().clean()


    def __str__(self):
        return self.username




