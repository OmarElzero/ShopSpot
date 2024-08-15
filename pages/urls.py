from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('shop', views.shop, name='shop'),
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'),
    path('registration_page', views.registration_page, name='registration_page'),
    path('login_page', views.login_page, name='login_page'),
    path('register/', views.registration_page, name='register'),
    path('login', views.user_login, name='user_login'),
    path('logout', views.user_logout, name='logout'),

]