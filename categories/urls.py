from django.urls import path
from . import views
from rest_framework import routers
router = routers.DefaultRouter()
urlpatterns = router.urls
urlpatterns+= [
    # path('product/<int:product_id>/', views.product_details, name='product_details'),
    # path('cart/', views.cart_page, name='cart'),
    # path('add_to_cart/<int:product_id>', views.add_to_cart, name='add_to_cart'),
    # path('remove-from-cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    # path('clear-cart/', views.clear_cart, name='clear_cart'),
    # path('filter_by_category/<int:category_id>/', views.filter_by_category, name='filter_by_category'),
    # path('search/', views.search_products, name='search_products'),
    # path('view_ordered_items/', views.view_ordered_items, name='view_ordered_items'),
    # path('order_now/<int:product_id>/', views.order_now, name='order_now'),
    # path('cart_order_now/', views.cart_order_now, name='cart_order_now'),
]