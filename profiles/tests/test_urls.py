from django.test import SimpleTestCase
from django.urls import reverse, resolve
from profiles.views import login, logout, viewset_customer
from categories.views import viewset_product, viewset_cartItem, viewset_cart, viewset_category, viewset_orderItem, viewset_order

class TestUrls(SimpleTestCase):

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func, login)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, logout)

    def test_profile_url_resolves(self):
        url = reverse('customer-list')
        self.assertEquals(resolve(url).func.cls, viewset_customer)
      