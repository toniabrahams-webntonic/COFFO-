"""Views for user registration and authentication.

Small wrappers around Django authentication utilities to handle signup,
login and logout flows used by the site. Messages are used to provide
feedback to users. The signup form uses ``SignupForm`` to ensure widget
attributes are applied server-side.
"""

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from .forms import SignupForm


def signup(request):
    """Handle user signup using ``SignupForm``.

    On POST the form is validated and the new user is created. A
    success message is shown and the user is redirected to the login
    page (you may want to log the user in automatically instead).
    """

    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Account successfully created')

            # Redirect to login after successful registration
            return redirect('/registration/login/')
    else:
        form = SignupForm()

    return render(request, 'registration/signup.html', {
        'form': form
    })


def loginPage(request):
    """Authenticate and log a user in.

    The view reads the posted username/password and uses
    ``authenticate``/``login``. On failure an informational message is
    displayed. Consider adding rate limiting or throttling for
    production use to mitigate brute-force attacks.
    """

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'registration/login.html', context)


def LogoutUser(request):
    """Log the current user out and redirect to the login page."""

    logout(request)
    return redirect('/registration/login/')