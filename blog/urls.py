"""URL configuration for the blog application.

Defines the URL patterns used by the blog app and exposes a
namespace via ``app_name`` so reverse lookups can be performed as
``reverse('blog:post_list')`` and similar.
"""

from django.urls import path
from . import views

# Application namespace for URL reversing (used in templates and code)
app_name = 'blog'

# URL patterns for this app. Names are used for reverse lookups.
urlpatterns = [
    # List view for all published posts (first page)
    path('', views.post_list, name='post_list'),

    # List view filtered by category slug (e.g. /category/coffee/)
    path('category/<slug:category_slug>/', views.post_list, name='post_list_by_category'),

    # Detail view for a single post identified by its slug
    path('<slug:slug>/', views.post_detail, name='post_detail'),
]
