
from .models import CartItem, Cart,Category,OrderItem,Order

from . models import Product
from .serializers import ProductSerializer,CartItemSerializer,CartSerializer,CategorySerializer
from rest_framework import viewsets, status
from django.core.exceptions import ValidationError
from profiles.models import Customer
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from .models import Product
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product
from .serializers import ProductSerializer,OrderItemSerializer,OrderSerializer
from .filters import ProductFilter
from django.core.exceptions import PermissionDenied







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
        elif self.action in ['update', 'partial_update']:
            if self.request.user.is_staff or self.request.user.is_superuser or int(self.request.user.customer.id) == int(self.kwargs['pk']):
                return [IsAuthenticated()]
            else:
                raise PermissionDenied()
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        customer_id = self.request.session.get('customer_id')
        if customer_id is None:
            return Response({'error': 'You must be logged in to create a product.'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            customer = Customer.objects.filter(pk=customer_id).first()
        except Customer.DoesNotExist:
            return Response({'error': 'Invalid customer. Please log in again.'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer.save(seller=customer)
    def perform_destroy(self, instance):
        customer = self.request.user.customer
        user = instance.seller
        if user == customer or user.is_staff or user.is_superuser:
            instance.delete()
        else:
            return Response({'error': f"You cannot delete another seller's product '{instance.name}'"}, status=status.HTTP_403_FORBIDDEN)



#endpoint for category
class viewset_category(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        return [IsAuthenticated()]
#endpoint for cartitem    
class viewset_cartItem(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def get_permissions(self):
        if self.action in [ 'list']:
            if self.request.user.is_staff or self.request.user.is_superuser:
                return [IsAuthenticated()]
            else:
                raise PermissionDenied()
                # return [AllowAny()]
        elif self.action in ['create']:
                return [AllowAny()]
        else:
            raise PermissionDenied()

    def perform_create(self, serializer):
        cart_item = serializer.save()
        product = cart_item.item
        customer = self.request.user.customer # here
        if product.seller == customer:
              return Response({'error' : f"You cannot add your own product '{product.name}' to the cart"},status.HTTP_403_FORBIDDEN)
        # Decrease the quantity of the product by the quantity in the cart item
        if product.quantity >= cart_item.quantity:
            product.quantity -= cart_item.quantity
            product.save()
        else:
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
        # Get the cart associated with the CartItem
        cart = Cart.objects.filter(items=instance).first()
        if not cart:
            raise PermissionDenied("This cart item does not belong to any cart.")

        # Check if the cart belongs to the logged-in user
        if cart.user != self.request.user.customer:
            raise PermissionDenied("You are not allowed to delete this cart item.")
        
        if cart.user == self.request.user.customer:
            product = instance.item
            product.quantity += instance.quantity
            product.save()
            instance.delete()
        
        else:
            return Response({'error': 'You cannot delete another user\'s cart item.'}, status=status.HTTP_403_FORBIDDEN)

        

#endpoint for cart
class viewset_cart(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_permissions(self):
        if self.action in ['destroy', 'list']:
            if self.request.user.is_staff or self.request.user.is_superuser:
                return [IsAuthenticated()]
            else:
                raise PermissionDenied()
        elif self.action in [ 'update', 'partial_update', 'retrieve']:
            cart_id = self.kwargs.get('pk')
            cart = Cart.objects.get(pk=cart_id)
            if self.request.user.is_staff or self.request.user.is_superuser or cart.user == self.request.user.customer:
                return [IsAuthenticated()]
            else:
                raise PermissionDenied(
                    # depoug statment 
                    # {"error": f"You are not allowed to perform this action because user for cart is {cart.user} and you are {self.request.user.customer}."}
                )
        else:
            raise PermissionDenied()
        
       

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

#endpoint for orderItem
class viewset_orderItem(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            if self.request.user.is_staff or self.request.user.is_superuser:
                return [IsAuthenticated()]
            else:
                raise PermissionDenied()
        elif self.action in ['retrieve','destroy']:
            if self.request.user.is_staff or self.request.user.is_superuser or int(self.request.user.customer.id) == int(self.kwargs['pk']):
                return [IsAuthenticated()]
            else:
                raise PermissionDenied()
        else:
            return [IsAuthenticated()]
            
    def perform_create(self, serializer):
        user = self.request.user
        customer = Customer.objects.get(user=user)
        Order.objects.create(user=customer)

#endpoint for order
class viewset_order(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer






