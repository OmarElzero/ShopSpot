from django.db import models
from django.contrib.auth.models import User
from django.apps import AppConfig
from django.core.exceptions import ValidationError
from profiles.models import Customer
from rest_framework.response import Response
import profiles.models
from rest_framework import viewsets, status

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

def get_default_seller():
        return Customer.objects.first().id
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    image = models.URLField(null=True, blank=True)
    color = models.CharField(max_length=50)  # Add color field
    size = models.CharField(max_length=20)  # Add size field
    seller = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name


class CartItem(models.Model):
    item = models.ForeignKey('Product', on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)  # Auto-calculated price
    is_ordered = models.BooleanField(default=False,editable=False) #will change it when ordered

    def save(self, *args, **kwargs):
        if self.quantity > self.item.quantity:

            return Response({'error' :f"Cannot add {self.quantity} units of {self.item.name}. Only {self.item.quantity} available."}, status.HTTP_400_BAD_REQUEST )

        self.price = self.item.price * self.quantity
        super().save(*args, **kwargs)

    def total(self):
        return self.price

    def __str__(self):
        return f'{self.quantity} x {self.item.name}'




class Cart(models.Model):
    user = models.OneToOneField(Customer, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)

    def total(self):
        total_price = 0
        for cart_item in self.items.all():
            total_price += cart_item.total()
        return total_price

    def __str__(self):
        return f"{self.user}-Cart"

    def get_items(self):
        return self.items.all()




class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    )

    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Order #{self.pk} - {self.user.username}"




class OrderItem(models.Model):
    ordered_items = models.ManyToManyField(Cart)

    def __str__(self):
        cart_items_summary = ", ".join(
            [f"{item.quantity} x {item.item.name}" for cart in self.ordered_items.all() for item in cart.items.all()]
        )
        return f"Order Items: {cart_items_summary}"

    def get_user_carts(self, user):
        return self.ordered_items.filter(user=user)

