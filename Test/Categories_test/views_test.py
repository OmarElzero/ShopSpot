import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from categories.models import CartItem, Product, Cart
from profiles.models import Customer
from django.contrib.auth.models import User

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='testpassword')

@pytest.fixture
def customer(user):
    return Customer.objects.create(user=user)

@pytest.fixture
def product(customer):
    return Product.objects.create(name='Test Product', seller=customer, quantity=10)

@pytest.fixture
def cart(customer):
    return Cart.objects.create(user=customer)

@pytest.fixture
def cart_item(cart, product):
    return CartItem.objects.create(cart=cart, item=product, quantity=1)

@pytest.mark.django_db
def test_create_cart_item(api_client, user, product):
    api_client.login(username='testuser', password='testpassword')
    url = reverse('cartitem-list')
    data = {
        'item': product.id,
        'quantity': 1
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert CartItem.objects.count() == 1

@pytest.mark.django_db
def test_create_cart_item_own_product(api_client, user, product):
    api_client.login(username='testuser', password='testpassword')
    url = reverse('cartitem-list')
    data = {
        'item': product.id,
        'quantity': 1
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_delete_cart_item(api_client, user, cart_item):
    api_client.login(username='testuser', password='testpassword')
    url = reverse('cartitem-detail', args=[cart_item.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert CartItem.objects.count() == 0

@pytest.mark.django_db
def test_delete_cart_item_not_owner(api_client, user, cart_item):
    another_user = User.objects.create_user(username='anotheruser', password='anotherpassword')
    api_client.login(username='anotheruser', password='anotherpassword')
    url = reverse('cartitem-detail', args=[cart_item.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert CartItem.objects.count() == 1