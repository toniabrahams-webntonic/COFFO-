"""Forms used by the core application (reviews and reservations)."""

from django import forms
from .models import Review, Reservation


class ReviewForm(forms.ModelForm):
    """Form for submitting a review.

    The rating field is represented as a RadioSelect with star labels
    for a more user-friendly UI. The review field uses a textarea
    with a small number of rows and Bootstrap classes for styling.
    """

    class Meta:
        model = Review
        fields = ['review', 'rating']
        widgets = {
            'review': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'rating': forms.RadioSelect(choices=[
                (5, '⭐⭐⭐⭐⭐'),
                (4, '⭐⭐⭐⭐☆'),
                (3, '⭐⭐⭐☆☆'),
                (2, '⭐⭐☆☆☆'),
                (1, '⭐☆☆☆☆'),
            ])
        }


class ReservationForm(forms.ModelForm):
    """Form used to create a Reservation.

    Widgets are configured to provide HTML5 date/time inputs and
    Bootstrap styling. The ``num_people`` field uses a Select element
    which can be filled with choices in the model or the form.
    """

    # this defines reservation form as a model form based on Reservation model
    class Meta:
        model = Reservation
        fields = ['name', 'email', 'reservation_date', 'reservation_time', 'num_people']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control inputs mb-3',
                'placeholder': 'Name',
                'required': 'required',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control inputs mb-2',
                'placeholder': 'Email',
                'required': 'required',
                'type': 'email'
            }),
            'reservation_date': forms.DateInput(attrs={
                'class': 'form-control inputs mb-2',
                'placeholder': 'Date',
                'required': 'required',
                'type': 'date'
            }),
            'reservation_time': forms.TimeInput(attrs={
                'class': 'form-control inputs mb-2',
                'placeholder': 'Time',
                'required': 'required',
                'type': 'time'
            }),
            'num_people': forms.Select(attrs={
                'class': 'form-control custom-select mb-2',
                'id': 'amount',
            }),
        }