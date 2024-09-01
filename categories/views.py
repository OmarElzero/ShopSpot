from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from .models import Product, CartItem, Cart, Category, Order, OrderItem
from profiles.forms import ProductSearchForm, RegistrationForm

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import reverse
from . models import Product
from .serializers import ProductSerializer,CartItemSerializer,CartSerializer
from rest_framework import viewsets
from django.core.exceptions import ValidationError
from profiles.models import Customer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password







# Create your views here.

#endpoint for products
class viewset_product(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        customer_id = self.request.session.get('customer_id')
        if not customer_id:
            raise ValidationError("You must be logged in to create a product.")
        try:
            customer = Customer.objects.get(pk=customer_id)
        except Customer.DoesNotExist:
            raise ValidationError("Invalid customer. Please log in again.")

        serializer.save(seller=customer)


class viewset_cartItem(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def perform_create(self, serializer):
        cart_item = serializer.save()
        product = cart_item.item
        customer = self.request.user.customer # here
        if product.seller == customer:
            raise ValidationError(f"You cannot add your own product '{product.name}' to the cart.")

        # Decrease the quantity of the product by the quantity in the cart item
        if product.quantity >= cart_item.quantity:
            product.quantity -= cart_item.quantity
            product.save()
        else:
            raise ValidationError(f"Not enough stock for {product.name}. Only {product.quantity} available.")

    def perform_destroy(self, instance):
        product = instance.item
        product.quantity += instance.quantity
        product.save()

        instance.delete()

class viewset_cart(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def perform_destroy(self, instance):
        for cart_item in instance.items.all():
            product = cart_item.item
            product.quantity += cart_item.quantity
            product.save()
            cart_item.delete()

        instance.delete()





