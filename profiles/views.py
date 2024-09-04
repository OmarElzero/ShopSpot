from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import Customer
from .serializers import CustomerSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError



class viewset_customer(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def perform_create(self, serializer):
        username = self.request.data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("A user with that username already exists.")

        user = User.objects.create_user(
            username=username,
            password=self.request.data.get('password')
        )
        serializer.save(user=user)

    #-------------------------BREAK FOR 5:40---------------------------------------------


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

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
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)