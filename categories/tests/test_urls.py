  
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from profiles.views import login, logout, viewset_customer
from categories.views import viewset_product, viewset_cartItem, viewset_cart, viewset_category, viewset_orderItem, viewset_order

class TestCategoryUrls(SimpleTestCase):

            def test_product_url_resolves(self):
                url = reverse('product-list')
                self.assertEquals(resolve(url).func.cls, viewset_product)

            def test_cart_item_url_resolves(self):
                url = reverse('cartitem-list')
                self.assertEquals(resolve(url).func.cls, viewset_cartItem)

            def test_cart_url_resolves(self):
                url = reverse('cart-list')
                self.assertEquals(resolve(url).func.cls, viewset_cart)

            def test_category_url_resolves(self):
                url = reverse('category-list')
                self.assertEquals(resolve(url).func.cls, viewset_category)

            def test_order_item_url_resolves(self):
                url = reverse('orderitem-list')
                self.assertEquals(resolve(url).func.cls, viewset_orderItem)

            def test_order_url_resolves(self):
                url = reverse('order-list')
                self.assertEquals(resolve(url).func.cls, viewset_order)