from django.test import TestCase
from django.contrib.auth.models import User
from profiles.models import Customer
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.core.management import call_command


class CustomerModelTest(TestCase):

    def setUp(self):
        call_command('flush', '--no-input')
        # Set up a user for the Customer model to reference
        self.user = User.objects.create(username="testuser", password="password123")
    
    def test_create_customer(self):
        """Test creating a Customer with all valid fields"""
        customer = Customer.objects.create(
            user=self.user,
            name="Test Customer",
            phone=1234567890,
            email="customer@example.com",
            address="123 Test St.",
            username="testcustomer",
            password="password123"
        )

        # Check if the customer is created successfully
        self.assertEqual(customer.name, "Test Customer")
        self.assertEqual(customer.phone, 1234567890)
        self.assertEqual(customer.email, "customer@example.com")
        self.assertEqual(customer.address, "123 Test St.")
        self.assertEqual(customer.username, "testcustomer")
        self.assertEqual(customer.password, "password123")
    
    def test_unique_email(self):
        """Test that the email must be unique"""
        Customer.objects.create(
            user=self.user,
            name="Customer1",
            phone=9876543210,
            email="uniqueemail@example.com",
            address="456 Another St.",
            username="customer1",
            password="password123"
        )

        # Try creating another customer with the same email and check for IntegrityError
        with self.assertRaises(IntegrityError):
            Customer.objects.create(
                user=self.user,
                name="Customer2",
                phone=1234567890,
                email="uniqueemail@example.com",  # Duplicate email
                address="789 Another St.",
                username="customer2",
                password="password123"
            )
    
    def test_unique_username(self):
        """Test that the username must be unique"""
        Customer.objects.create(
            user=self.user,
            name="Customer1",
            phone=9876543210,
            email="email1@example.com",
            address="456 Another St.",
            username="uniqueusername",
            password="password123"
        )

        # Try creating another customer with the same username and check for IntegrityError
        with self.assertRaises(IntegrityError):
            Customer.objects.create(
                user=self.user,
                name="Customer2",
                phone=1234567890,
                email="email2@example.com",
                address="789 Another St.",
                username="uniqueusername",  # Duplicate username
                password="password123"
            )
    
    def test_nullable_phone(self):
        """Test that the phone field can be null"""
        customer = Customer.objects.create(
            user=self.user,
            name="Customer No Phone",
            phone=None,
            email="customerwithoutphone@example.com",
            address="456 No Phone St.",
            username="customerwithoutphone",
            password="password123"
        )
        self.assertIsNone(customer.phone)
    
    def test_str_method(self):
        """Test the __str__ method of Customer"""
        customer = Customer.objects.create(
            user=self.user,
            name="Test Customer",
            phone=1234567890,
            email="customer@example.com",
            address="123 Test St.",
            username="testcustomer",
            password="password123"
        )
        self.assertEqual(str(customer), "testcustomer")

    def test_customer_without_required_fields(self):
        """Test creating a customer without required fields should raise an error"""
        with self.assertRaises(ValidationError):
            customer = Customer(
                user=self.user,
                name="Customer Without Email",
                phone=1234567890,
                address="No email address",
                username="customerwithoutemail",
                password="password123"
            )
            customer.full_clean()  # This should raise a ValidationError

    def test_phone_field_validation(self):
        """Test if invalid phone numbers (too short) raise a validation error"""
        with self.assertRaises(ValidationError):
            customer = Customer(
                user=self.user,
                name="Short Phone Customer",
                phone=12345,  # Too short phone number
                email="shortphonecustomer@example.com",
                address="789 Short Phone St.",
                username="shortphonecustomer",
                password="password123"
            )
            customer.full_clean()  # Should raise a validation error due to short phone number
