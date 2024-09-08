import random
import requests
from django.core.management.base import BaseCommand
from faker import Faker
from categories.models import Product, Category, Customer  # Update with your actual app name



class Command(BaseCommand):
    help = 'Generate fake e-commerce products for testing'

    def handle(self, *args, **kwargs):
        fake = Faker()
        categories = Category.objects.all()
        customers = Customer.objects.all()

        if not categories.exists() or not customers.exists():
            self.stdout.write(self.style.ERROR("Please ensure you have categories and customers in the database."))
            return

        product_names = {
            'Electronics': [
                'Smartphone', 'Laptop', 'Headphones', 'Tablet', 'Smart TV',
                'Camera', 'Smartwatch', 'Bluetooth Speaker', 'Drone', 'Keyboard'
            ],
            'Fashion': [
                'T-shirt', 'Jeans', 'Jacket', 'Dress', 'Sneakers',
                'Watch', 'Sunglasses', 'Hat', 'Scarf', 'Belt'
            ],
            'Home & Kitchen': [
                'Blender', 'Coffee Maker', 'Desk Lamp', 'Refrigerator', 'Microwave Oven',
                'Toaster', 'Cookware Set', 'Air Purifier', 'Vacuum Cleaner', 'Washing Machine'
            ],
            'Sports': [
                'Fitness Tracker', 'Bicycle', 'Helmet', 'Tent', 'Sleeping Bag',
                'Yoga Mat', 'Dumbbells', 'Treadmill', 'Basketball', 'Soccer Ball'
            ],
            'Beauty': [
                'Perfume', 'Makeup Kit', 'Handbag', 'Leather Wallet', 'Skincare Set',
                'Hair Dryer', 'Nail Polish', 'Hair Straightener', 'Body Lotion', 'Shaving Kit'
            ],
            'Automotive': [
                'Car Cover', 'GPS Navigation', 'Dash Cam', 'Car Charger', 'Seat Covers',
                'Bluetooth Adapter', 'Portable Vacuum', 'Roof Rack', 'Car Cleaning Kit', 'Jump Starter'
            ],
            'Books': [
                'Fiction Novel', 'Non-fiction Book', 'Biography', 'Cookbook', 'Science Fiction',
                'Historical Novel', 'Self-help Book', 'Travel Guide', 'Children\'s Book', 'Graphic Novel'
            ],
            'Toys': [
                'Action Figure', 'Doll', 'Puzzle', 'Board Game', 'Building Blocks',
                'Remote Control Car', 'Stuffed Animal', 'Educational Toy', 'Toy Train', 'Toy Kitchen Set'
            ],
            'Pet Supplies': [
                'Dog Food', 'Cat Food', 'Pet Bed', 'Pet Carrier', 'Dog Leash',
                'Cat Toy', 'Pet Grooming Kit', 'Pet Brush', 'Pet Shampoo', 'Pet Training Pads'
            ]
        }

        sizes = ['S', 'M', 'L', 'XL', 'XXL']
        colors = ['Red', 'Blue', 'Green', 'Black', 'White', 'Yellow', 'Pink', 'Orange', 'Purple', 'Gray']

        for category in categories:
            if category.name in product_names:
                self.stdout.write(self.style.SUCCESS(f"Generating products for category: {category.name}"))
                for _ in range(10):  # Adjust the number of products per category
                    product_name = random.choice(product_names[category.name])
                    product = Product.objects.create(
                        name=product_name,
                        description=fake.text(max_nb_chars=200),  # Longer product description
                        price=round(random.uniform(5.99, 1999.99), 2),  # Prices between $5.99 and $1999.99
                        quantity=random.randint(1, 1000),  # Random stock between 1 and 1000
                        category=category,
                        color=random.choice(colors),
                        size=random.choice(sizes),
                        seller=random.choice(customers),
                        image=f"https://picsum.photos/200/300"
                        # Fetch product-specific images from Pexels
                    )
                    self.stdout.write(
                        self.style.SUCCESS(f"Created product: {product.name} in category {category.name}"))

        self.stdout.write(self.style.SUCCESS("Successfully generated fake e-commerce products!"))


