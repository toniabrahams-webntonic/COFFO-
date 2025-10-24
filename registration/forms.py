"""User signup form.

This module defines a SignupForm subclassing Django's
UserCreationForm and configures widget attributes for nicer
presentation. Using widget attrs here avoids manipulating inputs via
client-side JS in templates.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User #provides username validation and password management


class SignupForm(UserCreationForm):
    """User registration form with custom widgets.

    The form exposes: username, email, password1, password2. Widget
    attributes set here control placeholders and CSS classes used by
    the templates.
    """

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username', # this is for user guidance
        'class': 'w-full float-left text-base text-gray-800 bg-gray-200 px-6 py-2.5 mt-1 border-0 rounded-full font-sans'
    }))

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Your email address', 
        'class': 'w-full float-left text-base text-gray-800 bg-gray-200 px-6 py-2.5 mt-1 border-0 rounded-full font-sans'
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class': 'w-100 float-start fs-6 text-dark bg-light px-3 py-2 mt-1 border-0 rounded-pill font-monospace'
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repeat password',
        'class': 'w-100 float-start fs-6 text-dark bg-light px-3 py-2 mt-1 border-0 rounded-pill font-monospace'
    }))
