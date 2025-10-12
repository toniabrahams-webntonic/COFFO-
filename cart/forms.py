"""Forms used by the cart views.

Currently includes a simple form used to add products to the cart.
The ``update`` field is a hidden boolean used to indicate whether the
quantity should be replaced or incremented.
"""

from django import forms


class CartAddProductForm(forms.Form):
    # Quantity to add or set for the product
    quantity = forms.IntegerField(
        min_value=1,
        max_value=20,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    # Hidden field used by the view to decide whether to update (set)
    # the quantity or increment the existing one.
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)