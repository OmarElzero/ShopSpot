from django.urls import path,include
from . import views
from rest_framework import routers
from rest_framework import viewsets , generics,mixins
router = routers.DefaultRouter()
router.register('customer',views.viewset_customer)
# urlpatterns = router.urls
urlpatterns = [

path('profile/', include(router.urls)),
    path('login/', views.login),


]