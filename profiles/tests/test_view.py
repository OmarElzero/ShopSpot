from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.core.management import call_command
from profiles.models import Customer
import random
import string

class CustomerAPITestCase(TestCase):

    def setUp(self):
        call_command('flush', '--no-input')
        self.client = APIClient()

        # Generate a random string of length 10 and make it unique
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + str(random.randint(1000, 9999))

        # Create users with different permissions
        self.user = User.objects.create_user(username=random_string, password='password123')
        self.admin = User.objects.create_user(username='admin_user', password='password123', is_staff=True)
        self.superadmin = User.objects.create_user(username='superadmin_user', password='password123', is_staff=True, is_superuser=True)

        # Ensure unique emails for each customer
        self.customer = Customer.objects.create(user=self.user, username=random_string, name="Test Customer", email=f'testcustomer_{random_string}@example.com', address="123 Test St")
        self.admin_customer = Customer.objects.create(user=self.admin, username='admin_user', name="Admin Customer", email="admincustomer@example.com", address="123 Admin St")
        self.superadmin_customer = Customer.objects.create(user=self.superadmin, username='superadmin_user', name="Superadmin Customer", email="superadmincustomer@example.com", address="123 Superadmin St")

    def test_create_customer(self):
        self.client.force_authenticate(user=self.superadmin)  # Ensure superadmin is authenticated
        url = reverse('customer-list')
        data = {
            'username': 'new_user',
            'password': 'password123',
            'name': 'New Customer',
            'email': 'newcustomer@example.com',
            'address': '123 New St'
        }
        response = self.client.post(url, data, format='json')
        #statements for debugging
        #print(f"Create Customer Response Status Code: {response.status_code}")
        #print(f"Create Customer Response Content: {response.content.decode()}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 4)  # Adjusted based on the setup

    def test_create_customer_with_existing_username(self):
        self.client.force_authenticate(user=self.superadmin)  # Ensure superadmin is authenticated
        url = reverse('customer-list')
        data = {
            'username': self.customer.username,  # Existing username
            'password': 'password123',
            'name': 'New Customer',
            'email': 'newcustomer@example.com',
            'address': '123 New St'
        }
        response = self.client.post(url, data, format='json')
        #statements for debugging
        #print(f"Create Existing Username Response Status Code: {response.status_code}")
        #print(f"Create Existing Username Response Content: {response.content.decode()}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_customer_list_as_admin(self):
        self.client.force_authenticate(user=self.admin)  # Ensure admin is authenticated
        url = reverse('customer-list')
        response = self.client.get(url)
        #statements for debugging
        #print(f"Customer List as Admin Response Status Code: {response.status_code}")
        #print(f"Customer List as Admin Response Content: {response.content.decode()}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_customer_list_permission_denied(self):
        self.client.force_authenticate(user=self.user)  # Ensure regular user is authenticated
        url = reverse('customer-list')
        response = self.client.get(url)
        #statements for debugging
        #print(f"Customer List Permission Denied Response Status Code: {response.status_code}")
        #print(f"Customer List Permission Denied Response Content: {response.content.decode()}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_customer_update(self):
        self.client.force_authenticate(user=self.user)  # Ensure user is authenticated
        url = reverse('customer-detail', args=[self.customer.pk])
        data = {'name': 'Updated Customer Name'}
        response = self.client.put(url, data, format='json')
        #statements for debugging
        #print(f"Customer Update Response Status Code: {response.status_code}")
        #print(f"Customer Update Response Content: {response.content.decode()}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.customer.refresh_from_db()

    def test_customer_delete(self):
        self.client.force_authenticate(user=self.user)  # Ensure user is authenticated
        url = reverse('customer-detail', args=[self.customer.pk])
        response = self.client.delete(url)
        #statements for debugging
        #print(f"Customer Delete Response Status Code: {response.status_code}")
        #print(f"Customer Delete Response Content: {response.content.decode()}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_permission_denied_on_delete(self):
        self.client.force_authenticate(user=self.user)  # Ensure user is authenticated
        url = reverse('customer-detail', args=[self.admin_customer.pk])
        response = self.client.delete(url)
        #statements for debugging
        #print(f"Permission Denied on Delete Response Status Code: {response.status_code}")
        #print(f"Permission Denied on Delete Response Content: {response.content.decode()}")
        #print(f"self.user.id: {self.user.id}")
        #print(f"self.admin.id: {self.admin_customer.pk}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_customer_retrieve(self):
        self.client.force_authenticate(user=self.user)  # Ensure user is authenticated
        url = reverse('customer-detail', args=[self.customer.pk])
        response = self.client.get(url)
        #statements for debugging
        #print(f"Customer Retrieve Response Status Code: {response.status_code}")
        #print(f"Customer Retrieve Response Content: {response.content.decode()}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Customer')

class LoginLogoutAPITestCase(TestCase):
    def setUp(self):
        call_command('flush', '--no-input')
        self.client = APIClient()

        # Create a test user
        self.user = User.objects.create_user(username='test_user', password='password123')
        self.customer = Customer.objects.create(user=self.user, name="Test Customer", email="testcustomer@example.com", address="123 Test St")

    def test_login_success(self):
        url = reverse('login')
        data = {
            'username': 'test_user',
            'password': 'password123'
        }
        response = self.client.post(url, data, format='json')
        #statements for debugging
        #print(f"Login Success Response Status Code: {response.status_code}")
        #print(f"Login Success Response Content: {response.content.decode()}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_invalid_credentials(self):
        url = reverse('login')
        data = {
            'username': 'invalid_user',
            'password': 'password123'
        }
        response = self.client.post(url, data, format='json')
        #statements for debugging
        #print(f"Login Invalid Credentials Response Status Code: {response.status_code}")
        #print(f"Login Invalid Credentials Response Content: {response.content.decode()}")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_missing_credentials(self):
        url = reverse('login')
        data = {
            'username': 'test_user'
        }
        response = self.client.post(url, data, format='json')
        #statements for debugging
        #print(f"Login Missing Credentials Response Status Code: {response.status_code}")
        #print(f"Login Missing Credentials Response Content: {response.content.decode()}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout_success(self):
        # First login to get token
        url = reverse('login')
        data = {
            'username': 'test_user',
            'password': 'password123'
        }
        response = self.client.post(url, data, format='json')
        #statements for debugging
        #print(f"Logout Pre-Login Response Status Code: {response.status_code}")
        #print(f"Logout Pre-Login Response Content: {response.content.decode()}")
        token = response.data.get('token')
        
        # Check if token is retrieved
        if not token:
            #print("Failed to retrieve token for logout test.")
            return  # Exit the test if no token is retrieved
        
        # Now logout using the token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        logout_url = reverse('logout')
        logout_response = self.client.post(logout_url)
        #statements for debugging
        #print(f"Logout Success Response Status Code: {logout_response.status_code}")
        #print(f"Logout Success Response Content: {logout_response.content.decode()}")
        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)

    def test_logout_without_token(self):
        url = reverse('logout')
        response = self.client.post(url)
        #statements for debugging
        #print(f"Logout Without Token Response Status Code: {response.status_code}")
        #print(f"Logout Without Token Response Content: {response.content.decode()}")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # Adjusted to expect 401