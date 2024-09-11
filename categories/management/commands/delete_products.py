from django.core.management.base import BaseCommand
from categories.models import Product  # Update with your actual app name

class Command(BaseCommand):
    help = 'Delete all products from the database'

    def handle(self, *args, **kwargs):
        product_count = Product.objects.count()

        if product_count == 0:
            self.stdout.write(self.style.WARNING('No products found in the database.'))
        else:
            Product.objects.all().delete()  # Deletes all products
            self.stdout.write(self.style.SUCCESS(f'Successfully deleted {product_count} products from the database.'))
