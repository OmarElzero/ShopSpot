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



#
# @api_view(['GET', 'PUT', 'DELETE'])
# def customer_information(request, id):
#     if request.method == 'GET':
#             try:
#                 customer = Customer.objects.get(pk=id)
#                 serializer = CustomerSerializer(customer)
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             except Customer.DoesNotExist:
#                 return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)
#
#
#
#
#
#     elif request.method == 'PUT':
#         try:
#             customer = Customer.objects.get(pk=id)
#             serializer = CustomerSerializer(customer, data=request.data, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Customer.DoesNotExist:
#             return Response({'error': 'Customer not found2'}, status=status.HTTP_404_NOT_FOUND)
#
#     elif request.method == 'DELETE':
#         try:
#             customer = Customer.objects.get(pk=id)
#             customer.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         except Customer.DoesNotExist:
#             return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)
#
#
#
# @api_view(['POST' ,'GET'])
# def post_customer(request):
#     if request.method == 'POST':
#         username = request.data.get('username')
#         email = request.data.get('email')
#         if Customer.objects.filter(Q(username=username) | Q(email=email)).exists():
#             return Response({'error': 'Customer already exists'}, status=status.HTTP_400_BAD_REQUEST)
#
#         serializer = CustomerSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'GET':
#         customers = Customer.objects.all()
#         serializer = CustomerSerializer(customers, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

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
        authenticate(username=username, password=password)
        token = Token.objects.get_or_create(user=customer)
        if customer.password == password:
            # Store the customer ID in the session after a successful login
            request.session['customer_id'] = customer.id
            return Response({'success': True, 'token': token},status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    except Customer.DoesNotExist:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)