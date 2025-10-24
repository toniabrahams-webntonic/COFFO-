"""Views for the cart application.

Provides product listing/detail pages and a small API for manipulating
the session-backed cart (add, remove, clear). Views that modify state
use the ``require_POST`` decorator to avoid side effects on GET requests.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

# Local application imports
from .models import Product  # Product model used to list and lookup products
from .cart import Cart
from .forms import CartAddProductForm


def product_list(request):
    """Render a list of available products.

    Returns the ``cart/product_list.html`` template with a ``products``
    context variable containing available Product instances.
    """
    # view for displaying list of products
    products = Product.objects.filter(available=True) 
    return render(request, 'cart/product_list.html', {'products': products})


def product_detail(request, slug):
    """Show product details and a small form to add the product to cart.

    The view returns a default ``CartAddProductForm`` instance which the
    template renders for posting to the ``cart_add`` view.
    """

    product = get_object_or_404(Product, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'cart/product_detail.html', {
        'product': product,
        'cart_product_form': cart_product_form,
    })


@require_POST # Only accept POST requests, it handles both add and update
def cart_add(request, product_id):
    """Add a product to the cart or update its quantity.

    This view only accepts POST requests. It validates the posted
    ``CartAddProductForm`` and then uses the Cart API to add or set the
    quantity for the chosen product.
    """

    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
    # Redirect to the cart detail page after adding
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    """Remove a product from the cart and redirect to the cart detail."""

    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product) # Remove the product from the cart using the Cart API
    return redirect('cart:cart_detail') #reirects to show upated site


def cart_detail(request):
    """Display the contents of the cart and provide update forms.

    For each item in the cart an ``update_quantity_form`` is injected so
    the template can render a small form allowing the user to change the
    quantity (which will POST back to the ``cart_add`` view with
    ``update=True``).
    """

    cart = Cart(request) # Get the cart current instance
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'update': True,
        })
    #iterate through cart items and add update form to each item
    return render(request, 'cart/cart_detail.html', {'cart': cart})


@require_POST
def cart_clear(request):
    """Clear the cart from the session and redirect to cart detail."""

    cart = Cart(request)
    cart.clear()
    return redirect('cart:cart_detail')