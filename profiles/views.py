
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


@login_required
def profile(request):
    user_details = request.user.customer
    return render(request, 'profiles/profile.html', {'user_details': user_details})


@login_required
def profile_edit(request):
    user_details = request.user.customer

    if request.method == 'POST':
        user_details.name = request.POST['name']
        user_details.phone = request.POST['phone']
        user_details.email = request.POST['email']
        user_details.address = request.POST['address']
        user_details.save()
        return redirect('profile')

    return render(request, 'profiles/profile_edit.html', {'user_details': user_details})

