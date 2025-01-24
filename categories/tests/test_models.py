from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from profiles.models import Customer
from categories.models import Category, Product, CartItem, Cart, Order, OrderItem
from decimal import Decimal
import random
import time
import uuid
from django.core.management import call_command

class ShopModelsTest(TestCase):
    def setUp(self):
        call_command('flush', '--no-input')

        unique_username = f'test_user_{uuid.uuid4().hex}'
        unique_email = f'unique_test_{uuid.uuid4().hex}@example.com'

        self.user = User.objects.create_user(username=unique_username, password='password123')
        self.customer = Customer.objects.create(user=self.user, name='Test Customer', email=unique_email, address='123 Street')
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            name='Laptop',
            description='High performance laptop',
            price=Decimal('1500.00'),
            quantity=10,
            category=self.category,
            color='Black',
            size='15 inch',
            seller=self.customer
        )
        self.cart_item = CartItem.objects.create(item=self.product, quantity=2)
        self.cart = Cart.objects.create(user=self.customer)
        self.cart.items.add(self.cart_item)

    def test_category_representation(self):
        self.assertEqual(str(self.category), 'Electronics')

    def test_product_representation(self):
        self.assertEqual(str(self.product), 'Laptop')

    def test_cart_item_representation(self):
        self.assertEqual(str(self.cart_item), '2 x Laptop')

    def test_cart_representation(self):
        # Update the test to reflect the correct string representation based on the user’s string value
        self.assertEqual(str(self.cart), f'{self.customer.user}-Cart')
        # print(str(self.cart))  # or self.user.username
        # print(f'{self.customer.user}-Cart')  # or self.user.username

    def test_order_representation(self):
        order = Order.objects.create(user=self.customer, status='pending')
        # Make sure the username is included from the user object
        self.assertEqual(str(order), f'Order #{order.pk} - {self.user.username}')

    def test_cart_item_price(self):
        self.assertEqual(self.cart_item.price, Decimal('3000.00'))

    def test_cart_total_price(self):
        self.assertEqual(self.cart.total(), Decimal('6000.00'))

    def test_cart_item_quantity_limit(self):
        with self.assertRaises(ValidationError):
            CartItem.objects.create(item=self.product, quantity=20).full_clean()

    def test_order_item_representation(self):
        order_item = OrderItem.objects.create()
        order_item.ordered_items.add(self.cart)
        self.assertIn('2 x Laptop', str(order_item))

    def test_order_item_user_cart_retrieval(self):
        order_item = OrderItem.objects.create()
        order_item.ordered_items.add(self.cart)
        self.assertEqual(order_item.get_user_carts(self.customer).count(), 1)

    def tearDown(self):
        super().tearDown()  # To ensure the database is rolled back properly
        User.objects.all().delete()
        Customer.objects.all().delete()

