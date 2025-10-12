"""URL patterns for the registration app.

Provides simple authentication routes and uses the 'registration'
namespace for reverse lookups in templates and views.
"""

from django.urls import path
from . import views

app_name = 'registration'

# Authentication endpoints: login, signup and logout
urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.LogoutUser, name='logout'),
]
