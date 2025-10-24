"""Admin registration for cart models.

Registers the Product model with custom admin options to simplify
management of products (search, filtering, inline editing of price and
availability, etc.).
"""

from django.contrib import admin
from .models import Product


@admin.register(Product) 
class ProductAdmin(admin.ModelAdmin):
    # Columns displayed on the changelist page
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated']

    # Sidebar filters
    list_filter = ['available', 'created', 'updated']

    # Allow editing these fields directly on the changelist
    list_editable = ['price', 'available']

    # Automatically populate the slug field from the name
    prepopulated_fields = {'slug': ('name',)}

    # Fields to include in the admin search box
    search_fields = ['name', 'description']

    # Add a date-based drill-down by the created timestamp
    date_hierarchy = 'created'