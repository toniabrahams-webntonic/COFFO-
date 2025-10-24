"""Core site models: reviews, contact messages and reservations.

These models back small features used across the site: visitor reviews
with a star rating, a simple contact message model, and a reservation
model storing date/time and party size.
"""

from django.db import models
from django.contrib.auth.models import User


# Rating choices used by the Review model. Display strings include
# stars for readability in the admin and templates.
RATING = [
    (1, '⭐☆☆☆☆ - Poor'),
    (2, '⭐⭐☆☆☆ - Fair'),
    (3, '⭐⭐⭐☆☆ - Good'),
    (4, '⭐⭐⭐⭐☆ - Very Good'),
    (5, '⭐⭐⭐⭐⭐ - Excellent'),
]


class Review(models.Model):
    """Customer review with an optional linked user.

    Fields
    - user: optional FK to Django's User; set to NULL if the user is
      deleted to preserve the review content.
    - review: text body of the review.
    - rating: integer choice from 1 to 5 using the RATING choices above.
    - date: timestamp of creation.
    """

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Reviews"
        ordering = ['-date']

    def __str__(self):
        username = self.user.username if self.user else "Anonymous"
        return f"Review by {username} - {self.rating} stars"

    def get_rating_stars(self):
        """Return a simple star string representation for templates."""

        if self.rating:
            return '⭐' * self.rating + '☆' * (5 - self.rating)
        return "No rating"


class Contact(models.Model):
    """Simple contact message submitted by a visitor."""

    name = models.CharField(max_length=50)
    email = models.EmailField()
    phoneNumber = models.CharField(max_length=12)
    description = models.TextField()

    def __str__(self):
        return f'Message from {self.name}'


class Reservation(models.Model):
    """Reservation made by a visitor including party size and timing."""

    name = models.CharField(max_length=100) # Visitor's full name limited to 100 characters
    email = models.EmailField() # Visitor's email address for contact email validation
    reservation_date = models.DateField() # Date of the reservation
    reservation_time = models.TimeField()   # Time of the reservation
    num_people = models.IntegerField(   
        choices=[
            (1, '1 Person'),
            (2, '2 People'),
            (3, '3 People'),
            (4, '4 People'),
            (5, '5 People'),
            (6, '6 People'),
        ],
        help_text="Number of people"
    )   # Number of people in the reservation with choices

    class Meta:
        # Order reservations by date then time for sensible listing
        ordering = ['reservation_date', 'reservation_time']

    def __str__(self):
        return f'Reservation for {self.name} ({self.num_people} people) on {self.reservation_date} at {self.reservation_time}'
        # String representation showing key details