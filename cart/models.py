"""Models for the cart application.

Defines a simple Product model and includes commented-out models for
an alternative database-backed cart implementation (Cart and
CartItem). The live implementation uses a session-backed cart in
``cart/cart.py`` instead of the commented models.
"""

from django.db import models
from django.conf import settings
from django.urls import reverse


class Product(models.Model):
    """A sellable product used in the shop.

    Fields:
    - name, slug: identifying fields for display and URLs
    - description: detailed product description
    - price: Decimal price stored with two decimal places
    - image: uploaded image stored under MEDIA_ROOT/products/
    - available: whether the product can be purchased
    - created/updated: timestamps for admin and ordering
    """

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        # Order products by name by default
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Return the canonical URL for the product detail page."""

        return reverse('cart:product_detail', args=[self.slug])


# The following models are an optional database-backed cart
# implementation. They are currently commented out because the
# project uses a lightweight session-backed cart (see cart/cart.py).
#
# class Cart(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return f'Cart {self.id}'
#
#     def get_total_cost(self):
#         return sum(item.get_cost() for item in self.items.all())
#
# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
#
#     def __str__(self):
#         return f'{self.quantity} x {self.product.name}'
#
#     def get_cost(self):
#         return self.product.price * self.quantity