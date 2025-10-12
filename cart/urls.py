"""URL patterns for the cart application.

Defines routes for viewing the cart, modifying its contents and
browsing product listings. The ``app_name`` provides a namespace for
reverse lookups (e.g. ``reverse('cart:cart_add', args=[product.id])``).
"""

from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    # Cart detail and modification views
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('clear/', views.cart_clear, name='cart_clear'),

    # Product listing and detail pages within the cart app
    path('products/', views.product_list, name='product_list'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
]