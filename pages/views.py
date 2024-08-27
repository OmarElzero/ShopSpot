from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from profiles.forms import ProductSearchForm, RegistrationForm
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import reverse
from categories.models import Product, CartItem, Cart, Category, Order, OrderItem
from profiles.models import Customer
from django.http import HttpResponse

# Create your views here.


def index(request):
    products = Product.objects.filter(quantity__gt=0)
    return  HttpResponse("test")


def shop(request):
    products = Product.objects.filter(quantity__gt=0)
    return render(request, 'pages/shop.html', {'products': products})


def contact(request):
    return render(request,'pages/contact.html')


def about(request):
    return render(request,'pages/about.html')





def login_page(request):
      return render(request,'pages/login.html')



def registration_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )

            customer = Customer(
                user=user,
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address']
            )
            customer.save()

            return redirect('login_page')
    else:
        form = RegistrationForm()
    return render(request, 'pages/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        user_name = request.POST['user_name']
        pass_word = request.POST['pass_word']
        user = auth.authenticate(username=user_name, password=pass_word)

        if user is not None and not user.is_superuser:
            login(request, user)
            auth.login(request, user)
            return redirect('index')
        elif user is not None and user.is_superuser:
            messages.error(request, 'Invalid credentials.')
            return redirect('login_page')
        else:
            messages.error(request, 'Invalid credentials.')
            return redirect('login_page')
    else:
        return redirect('index')


def user_logout(request):
    auth.logout(request)
    return redirect('index')

