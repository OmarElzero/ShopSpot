from django.urls import path,include
from . import views
from rest_framework import routers
from rest_framework import viewsets , generics,mixins

router = routers.DefaultRouter()
urlpatterns = router.urls
router.register('Products', views.viewset_product)
router.register('cart_items', views.viewset_cartItem)
router.register('cart', views.viewset_cart)
urlpatterns = [
    path('Categories/', include(router.urls)),

]