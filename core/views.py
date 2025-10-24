"""Views for core site features: reviews, contact messages and reservations.

This module contains three small views:

- submit_review: authenticated users can create or update a single
  review tied to their account. Uses messages to provide feedback.
- contact: accept a simple contact form via POST and save a Contact
  instance for later processing.
- reserve: present and process a ReservationForm to create a
  reservation record.
"""

from django.shortcuts import render, redirect
from .models import Review, Contact
from .forms import ReviewForm, ReservationForm
from django.contrib import messages


def submit_review(request):
    """Create or update the authenticated user's review.

    Behavior:
    - If the user is not authenticated, redirect to the index with an
      error message.
    - On POST: attempt to find an existing Review for the current
      user. If found, update it; otherwise create a new Review tied to
      the user. Form validation errors are reported via messages and
      the user is redirected back to the index.
    """

    # Only allow logged-in users to submit reviews
    if not request.user.is_authenticated: #rejects anonymous users
        messages.error(request, 'You must be logged in to submit a review.')
        return redirect('index') #redirect to home page
 
    if request.method == 'POST':
        # If a review for this user already exists, edit it; otherwise
        # create a new one.
        try:
            existing_reviews = Review.objects.get(user=request.user)
            form = ReviewForm(request.POST, instance=existing_reviews)
            if form.is_valid():
                form.save()
                messages.success(request, 'Thank you! Your review has been updated.')
                return redirect('index') #reirects to home page and confirms a success message
            else:
                # If the form is invalid, provide some context to the
                # index template and show an error message.
                reviews = Review.objects.all().order_by('-date')[:3]
                messages.error(request, 'Please correct the errors below.')
                return render(request, 'index.html', {'reviews': reviews})

        except Review.DoesNotExist: #if no existing review is found, create a new one
            form = ReviewForm(request.POST) #this will create a new form instance   
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect('index')
            else:
                # Invalid form on create: show an error and redirect
                reviews = Review.objects.all().order_by('-date')[:3]
                messages.error(request, 'Please correct the errors below.')
                return redirect('index')

    # For non-POST requests simply redirect back to the home page
    return redirect('index')


def contact(request):
    """Accept a contact message submitted via POST and save it.

    The view reads simple form fields directly from ``request.POST``
    and creates a ``Contact`` instance. After saving, it shows an
    acknowledgement message and redirects back to the contact page.
    """

    if request.method == 'POST':
        # Read fields from the POST payload. No server-side form is
        # used here; consider replacing this with a Django Form for
        # validation if inputs need stricter checks.
        fname = request.POST.get("name")
        femail = request.POST.get("email")
        phone = request.POST.get("phone")
        desc = request.POST.get("desc")
        query = Contact(name=fname, email=femail, phoneNumber=phone, description=desc)
        query.save()
        messages.success(request, "Thanks For Contacting Us! We will get back to you soon")
        return redirect('core:contact')

    return render(request, 'contact.html')


def reserve(request):
    """Display and process a reservation form.

    On GET: render an empty ReservationForm. On POST: validate and save
    the reservation, then show a success message and redirect back to
    the reservation page.
    """

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thanks for Reserving with Us.")
            return redirect('core:reserve')
    else:
        form = ReservationForm()

    return render(request, 'reserve.html', {
        'form': form
    })