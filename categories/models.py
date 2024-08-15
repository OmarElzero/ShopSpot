from django.db import models
from django.contrib.auth.models import User
from django.apps import AppConfig

import profiles.models
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/%Y/%m/%d/')
    color = models.CharField(max_length=50)  # Add color field
    size = models.CharField(max_length=20)  # Add size field

    def __str__(self):
        return self.name


class CartItem(models.Model):
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    quantity = models.IntegerField()
    price = models.FloatField()
    is_ordered = models.BooleanField(default=False)

    def total(self):
        return (self.quantity * self.item.price)


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)

    def total(self):
        total_price = 0
        for cart_item in self.items.all():
            total_price += cart_item.total()
        return (total_price)


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Order #{self.pk} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - Qty: {self.quantity}"