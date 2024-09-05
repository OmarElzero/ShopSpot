import random
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

        # Expanded product names list
        product_names = [
            'Smartphone', 'Laptop', 'Headphones', 'Running Shoes', 'T-shirt', 'Watch', 'Backpack',
            'Blender', 'Coffee Maker', 'Desk Lamp', 'Tablet', 'Camera', 'Wireless Mouse', 'Keyboard',
            'Smart TV', 'Sneakers', 'Gaming Console', 'Vacuum Cleaner', 'Refrigerator', 'Microwave Oven',
            'Air Conditioner', 'Washing Machine', 'Electric Kettle', 'Toaster', 'Hair Dryer',
            'Electric Toothbrush', 'Smart Watch', 'Sunglasses', 'Jeans', 'Jacket', 'Dress',
            'Perfume', 'Makeup Kit', 'Handbag', 'Leather Wallet', 'Office Chair', 'Bookshelf',
            'LED Monitor', 'Speakers', 'Gaming Chair', 'Action Camera', 'Drone', 'Fitness Tracker',
            'Bicycle', 'Helmet', 'Tent', 'Sleeping Bag', 'Camping Stove', 'Electric Scooter'
        ]

        sizes = ['S', 'M', 'L', 'XL', 'XXL']
        colors = ['Red', 'Blue', 'Green', 'Black', 'White', 'Yellow', 'Pink', 'Orange', 'Purple', 'Gray']

        for _ in range(500):  # Adjust the number of products to generate
            product = Product.objects.create(
                name=random.choice(product_names),
                description=fake.text(max_nb_chars=200),  # Longer product description
                price=round(random.uniform(5.99, 1999.99), 2),  # Prices between $5.99 and $1999.99
                quantity=random.randint(1, 1000),  # Random stock between 1 and 1000
                category=random.choice(categories),
                color=random.choice(colors),
                size=random.choice(sizes),
                seller=random.choice(customers),
                # Use Unsplash to fetch product-specific images (e.g., electronics, clothing)
                image=f"https://picsum.photos/300/300?random={random.randint(1, 1000)}"  # Random product images
            )
            self.stdout.write(self.style.SUCCESS(f"Created product: {product.name}"))

        self.stdout.write(self.style.SUCCESS("Successfully generated fake e-commerce products!"))
