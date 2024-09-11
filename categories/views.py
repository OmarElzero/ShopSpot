from rest_framework.decorators import api_view,permission_classes

from .models import CartItem, Cart,Category,OrderItem,Order

from . models import Product
from .serializers import ProductSerializer,CartItemSerializer,CartSerializer,CategoriesSerializer
from rest_framework import viewsets, status
from django.core.exceptions import ValidationError
from profiles.models import Customer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
import django_filters
from .models import Product
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product
from .serializers import ProductSerializer,OrderitemSerializer,OrderSerializer
from .filters import ProductFilter
from rest_framework.generics import ListAPIView






# Create your views here.

#endpoint for products
class viewset_product(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter

    def get_permissions(self):
        if self.action in ['retrieve', 'list']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        customer_id = self.request.session.get('customer_id')
        if not customer_id:
            raise ValidationError("You must be logged in to create a product.")
        try:
            customer = Customer.objects.filter(pk=customer_id).first()
        except Customer.DoesNotExist:
            raise ValidationError("Invalid customer. Please log in again.")

        serializer.save(seller=customer)




class viewset_category(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        return [IsAuthenticated()]
class viewset_cartItem(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def perform_create(self, serializer):
        cart_item = serializer.save()
        product = cart_item.item
        customer = self.request.user.customer # here
        if product.seller == customer:
            # raise ValidationError(f"You cannot add your own product '{product.name}' to the cart")
              return Response({'error' : f"You cannot add your own product '{product.name}' to the cart"},status.HTTP_403_FORBIDDEN)
        # Decrease the quantity of the product by the quantity in the cart item
        if product.quantity >= cart_item.quantity:
            product.quantity -= cart_item.quantity
            product.save()
        else:
            # raise ValidationError(f"Not enough stock for {product.name}. Only {product.quantity} available.")
            return Response({'error' : f"Not enough stock for {product.name}. Only {product.quantity} available." },status=status.HTTP_400_BAD_REQUEST)
        cart, created = Cart.objects.get_or_create(user=customer)
        if cart.items.filter(item=cart_item.item).exists():
            # If the item already exists in the cart, update the quantity
            existing_cart_item = cart.items.get(item=cart_item.item)
            existing_cart_item.quantity += cart_item.quantity
            existing_cart_item.save()
        else:
            # Otherwise, add the new item to the cart
            cart.items.add(cart_item)

    def perform_destroy(self, instance):
        product = instance.item
        product.quantity += instance.quantity
        product.save()

        instance.delete()

class viewset_cart(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def perform_create(self, serializer):
        user = self.request.user
        try:
            # Fetch the Customer instance associated with the User
            customer = Customer.objects.get(user=user)
        except Customer.DoesNotExist:
            # Handle the error if no Customer is found
            raise ValidationError("Customer not found for the current user.")

        serializer.save(user=customer)
    def perform_destroy(self, instance):
        for cart_item in instance.items.all():
            product = cart_item.item
            product.quantity += cart_item.quantity
            product.save()
            cart_item.delete()

        instance.delete()


class viewset_orderItem(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderitemSerializer



    def perform_create(self, serializer):
        user = self.request.user
        customer = Customer.objects.get(user=user)
        Order.objects.create(user=customer)


class viewset_order(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer








