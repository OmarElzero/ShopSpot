from django.urls import path
from . import views
from rest_framework import routers
router = routers.DefaultRouter()
urlpatterns = router.urls
urlpatterns+= [

path('profile/', views.customer_information),
path('profile/<int:id>/', views.customer_information),

]