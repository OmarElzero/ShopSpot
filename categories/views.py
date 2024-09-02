from .models import CartItem, Cart

from . models import Product
from .serializers import ProductSerializer,CartItemSerializer,CartSerializer
from rest_framework import viewsets
from django.core.exceptions import ValidationError
from profiles.models import Customer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated






# Create your views here.

#endpoint for products
class viewset_product(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
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





