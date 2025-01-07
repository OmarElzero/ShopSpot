from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status, viewsets
from .models import Customer
from .serializers import CustomerSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import permission_classes
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate



class viewset_customer(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        elif self.action == 'list':
            if self.request.user.is_staff or self.request.user.is_superuser:
                return [IsAuthenticated()]
            else:
                raise PermissionDenied()
        elif self.action in ['retrieve', 'update', 'partial_update']:
            if self.request.user.is_staff or self.request.user.is_superuser or int(self.request.user.customer.id) == int(self.kwargs['pk']):
                return [IsAuthenticated()]
            else:
                raise PermissionDenied()
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        username = self.request.data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError({'error': 'Username already exists'})

        if 'admin' in username:
            user = User.objects.create_user(
                username=username,
                password=self.request.data.get('password'),
                is_staff=True
            )
        elif 'superadmin' in username:
            user = User.objects.create_user(
                username=username,
                password=self.request.data.get('password'),
                is_staff=True,
                is_superuser=True
            )
        else:
            user = User.objects.create_user(
                username=username,
                password=self.request.data.get('password')
            )
        serializer.save(user=user)
        customer = getattr(user, 'customer', None)

    def perform_destroy(self, instance):
        user = self.request.user
        try:
            customer = user.customer
        except Customer.DoesNotExist:
            return Response({'error': 'You do not have a related customer.'}, status=status.HTTP_400_BAD_REQUEST)

        if customer.id == instance.id or user.is_staff or user.is_superuser:
            user = customer.user
            Token.objects.filter(user=user).delete()
            customer.delete()
            user.delete()
        else:
            return Response({'error': 'You are not allowed to delete this customer.'}, status=status.HTTP_403_FORBIDDEN)







@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username_or_email = request.data.get('username')
    password = request.data.get('password')

    if not username_or_email or not password:
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
    if '@' in username_or_email:
        try:
            user = Customer.objects.get(email=username_or_email)
            username_or_email = user.username
        except ObjectDoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, username=username_or_email, password=password)

    if user is not None:
        # Get or create a token for the authenticated user
        token, created = Token.objects.get_or_create(user=user)

        return Response({'success': True, 'token': token.key}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def logout(request):
    try:
        token = request.auth

        if token:
            token.delete()
            return Response({'success': True, 'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Token not found'}, status=status.HTTP_400_BAD_REQUEST)
    except Token.DoesNotExist:
        return Response({'error': 'Token does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)