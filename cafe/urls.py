"""URL configuration for the cafe project.

This module declares the root URL patterns for the site and delegates
to application-specific URLconfs such as `blog`, `cart` and
`registration`. Static media files are served during development by
appending the result of ``static(...)`` when ``settings.DEBUG`` is
enabled.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views # project-level views because they span multiple apps

# Root URL dispatch table. The order matters: more specific routes
# this means that routes defined earlier take precedence over later ones.
urlpatterns = [
    path('admin/', admin.site.urls),

    # Core site pages handled by the project-level `views` module
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('coffees/', views.coffees, name='coffees'),
    path('shop/', views.shop, name='shop'),
    # contact view is currently commented out
    # path('contact/', views.contact, name='contact'),

    # Search page (aggregates results across apps)
    path('search/', views.search, name='search'),

    # Delegate blog/cart/registration URL handling to their apps and
    # use namespaces to avoid reverse() name collisions.
    path('blog/', include('blog.urls', namespace='blog')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('registration/', include('registration.urls', namespace='registration')),

    # Include core app URLs. Placed last so it doesn't shadow other
    # more specific routes defined above.
    path('', include('core.urls')),
]

# During development serve media files from MEDIA_URL using Django's
# static() helper. In production, a front-end webserver or CDN should
# serve media files instead.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)