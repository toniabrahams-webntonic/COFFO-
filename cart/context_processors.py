"""Context processors for the cart app.

Provides a ``cart`` variable in template contexts which contains the
session-backed Cart instance for the current request/user.
"""

from .cart import Cart


def cart(request):
    """Return a mapping to inject the Cart into template contexts."""

    return {'cart': Cart(request)}