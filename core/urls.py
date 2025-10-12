"""URL patterns for the core application.

This module exposes endpoints for submitting reviews, contacting the
site, and making reservations. The ``app_name`` provides a namespace
for reversing URLs from templates or code (e.g. ``reverse('core:contact')``).
"""

from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('submit_review/', views.submit_review, name='submit_review'),
    path('contact/', views.contact, name='contact'),
    path('reserve/', views.reserve, name='reserve'),
]
