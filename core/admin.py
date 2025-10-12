"""Admin registrations for core models.

This module registers simple models (Review, Contact, Reservation)
with the Django admin site using default configuration. For more
advanced administration (custom list displays, filters, etc.) a
ModelAdmin subclass can be added.
"""

from django.contrib import admin
from .models import Review, Contact, Reservation


# Register the core models with the admin site using default behaviour.
admin.site.register(Review)
admin.site.register(Contact)
admin.site.register(Reservation)
