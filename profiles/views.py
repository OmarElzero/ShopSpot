from django.http import JsonResponse, HttpResponse, Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Customer
from .serializers import CustomerSerializer
from django.contrib.auth import authenticate
from .models import Customer
from django.db.models import Q
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def customer_information(request, id=None):
    # Fetch customer if pk is provided
    customer = None
    if id:
        try:
            customer = Customer.objects.get(pk=id)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        if id:
            serializer = CustomerSerializer(customer)
            return JsonResponse(serializer.data, safe=False)
        else:
            data = Customer.objects.all()
            serializer = CustomerSerializer(data, many=True)
            return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        username = request.data.get('username')
        email = request.data.get('email')
        if Customer.objects.filter(Q(username=username) | Q(email=email)).exists():
            return Response({'error': 'Customer already exists'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = CustomerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        serializer = CustomerSerializer(customer, data=request.data , partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if not customer:
            return Response({'error': 'Customer not found2'}, status=status.HTTP_404_NOT_FOUND)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return JsonResponse({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if user is not None:
        return JsonResponse({'success': True}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
