"""Application configuration for the shopping cart app."""

from django.apps import AppConfig


class CartConfig(AppConfig):
        """Configuration for the `cart` application.

        - ``name``: dotted Python path to the app module.
        - ``default_auto_field``: default auto field for model primary
            keys created in this app.
        - ``verbose_name``: human readable name used in the admin site.
        """

        default_auto_field = 'django.db.models.BigAutoField'
        name = 'cart'
        verbose_name = 'Shopping Cart'
