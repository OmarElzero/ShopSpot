from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import Customer
from .serializers import CustomerSerializer
from django.contrib.auth import authenticate
from django.db.models import Q
from django.contrib.auth import authenticate, login as auth_login
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate


class viewset_customer(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    #-------------------------BREAK FOR 5:40---------------------------------------------

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        customer = Customer.objects.get(username=username)

        if customer.password == password:
            # Store the customer ID in the session after a successful login
            request.session['customer_id'] = customer.id

            # Get or create a token for the customer
            token, created = Token.objects.get_or_create(user=customer)

            return Response({'success': True, 'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    except Customer.DoesNotExist:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)