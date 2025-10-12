"""Django settings for the `cafe` project with per-line explanations.

This file configures project-wide settings used by Django. It contains
constants for security, installed apps, middleware, templates, database
configuration, static/media files settings, and other framework options.

NOTE: Sensitive values like SECRET_KEY should not be committed to a public
repository for production use. The following comments explain each line.
"""

from pathlib import Path  # Import Path to build filesystem paths in a cross-platform way.

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# BASE_DIR points to the project's root directory (two levels up from this file).


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-vof2qlu^77ti2eg9%hiuh-y1)tvr*+cyk^fkxs)+e5okou%bj)'
# SECRET_KEY is used for cryptographic signing; replace it in production.

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG enables detailed error pages and auto-reloading; turn off in production.

ALLOWED_HOSTS = []
# ALLOWED_HOSTS lists hosts/domains the app can serve; empty during development.


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'blog',  # Custom app for blog posts and comments.
    'cart',  # Custom app that manages shopping cart functionality.
    'registration',  # Custom app for user registration and profiles.
    'core',  # Core app for shared models and utilities.
]
# INSTALLED_APPS registers Django and project apps with the framework.

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
# MIDDLEWARE is an ordered list of middleware classes executed per request.

ROOT_URLCONF = 'cafe.urls'
# ROOT_URLCONF points to the module that contains URL declarations for the project.

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS' lists directories where Django will search for templates.
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,  # Enable automatic template discovery inside app `templates/` dirs.
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart'  # Custom context processor to add cart to templates.
            ],
        },
    },
]
# TEMPLATES configures Django's template engine and global context processors.

WSGI_APPLICATION = 'cafe.wsgi.application'
# WSGI_APPLICATION is the callable used by WSGI servers to serve the project.


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Use SQLite as the database engine.
        'NAME': BASE_DIR / 'db.sqlite3',  # Database file located at project root.
    }
}
# DATABASES configures the project's database connections.


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
# AUTH_PASSWORD_VALIDATORS lists validators used when creating/changing passwords.


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'  # Default language code for the project.

TIME_ZONE = 'UTC'  # Time zone used by the project; change as needed.

USE_I18N = True  # Enable Django's translation system.

USE_TZ = True  # Use timezone-aware datetimes.


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'  # URL prefix for static files.
STATICFILES_DIRS = [BASE_DIR / 'static']  # Additional dirs for collectstatic to look for files.
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Directory where `collectstatic` will gather files for deployment.

MEDIA_URL = '/media/'  # URL prefix for user-uploaded media files.
MEDIA_ROOT = BASE_DIR / 'media'  # Filesystem directory for user-uploaded media.

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'  # Default field type for auto-generated primary keys.

CART_SESSION_ID = 'cart'  # Key used to store cart data in the user's session.
