from django.urls import path,include
from . import views
from rest_framework import routers
from rest_framework import viewsets , generics,mixins
from rest_framework.authtoken.views import obtain_auth_token
router = routers.DefaultRouter()
router.register('customer',views.viewset_customer)
# urlpatterns = router.urls
urlpatterns = [

path('profile/', include(router.urls)),
    path('login/', views.login),
path('logout/', views.logout)

# path('api-token-auth', obtain_auth_token),
#     path('api-auth', include('rest_framework.urls')),

]