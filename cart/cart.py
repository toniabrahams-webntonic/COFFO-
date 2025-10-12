"""Simple shopping cart backed by the user's session.

The Cart class provides a small API to add/remove products and to
iterate over items stored in the current session. Products are stored
in the session by their ID along with quantity and price at the time
they were added. The cart does not rely on any database object being
persisted for the lifetime of the session; instead it looks up the
Product objects on iteration to attach fresh model instances for
display in templates.
"""

from decimal import Decimal
from django.conf import settings
from .models import Product  # Use Product model from cart app


class Cart:
    """Session-backed shopping cart.

    Typical usage:
        cart = Cart(request)
        cart.add(product, quantity=2)
        for item in cart:
            display(item['product'], item['quantity'], item['total_price'])

    The cart stores prices as strings in the session to avoid serialization
    issues with Decimal objects; they are converted back to Decimal when
    iterating or computing totals.
    """

    def __init__(self, request):
        # Keep a reference to the session and load (or create) the cart
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Initialize an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """Add a product to the cart or update its quantity.

        If ``update_quantity`` is True, the quantity is set to the provided
        value. Otherwise the given quantity is added to any existing
        quantity for that product.
        """

        product_id = str(product.id)
        if product_id not in self.cart:
            # Store quantity and price (as string) to keep session serializable
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price),  # store as string for JSON/session safety
            }
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # Mark the session as modified so it will be saved by Django
        self.session.modified = True

    def remove(self, product):
        """Remove a product from the cart if present."""

        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """Iterate over the cart items, attaching Product instances.

        Yields items with keys: 'product' (model instance), 'price'
        (Decimal), 'quantity' (int) and 'total_price' (Decimal).
        """

        product_ids = self.cart.keys()
        # product_ids are stored as strings in the session; convert to ints for DB lookup
        try:
            product_ids_int = [int(pid) for pid in product_ids]
        except ValueError:
            # If conversion fails, fall back to using the string IDs
            product_ids_int = list(product_ids)

        # Fetch the Product objects for all IDs present in the cart
        products = Product.objects.filter(id__in=product_ids_int)
        cart = self.cart.copy()

        # Attach the product instances to the session data copy so templates
        # can access up-to-date model information (e.g. name, image)
        for product in products:
            cart[str(product.id)]['product'] = product

        # Convert stored price strings back to Decimal and compute totals
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Return total quantity of all items in the cart."""

        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Compute the cart's total price as a Decimal."""

        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """Remove the cart from the session."""

        if settings.CART_SESSION_ID in self.session:
            del self.session[settings.CART_SESSION_ID]
        self.save()