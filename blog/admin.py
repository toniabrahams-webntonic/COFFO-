"""Admin registrations for the blog app.

This module registers Category, Post and Comment models with the Django admin
site and configures how they are displayed and edited in the admin UI.
"""  # Module docstring: explains the file's purpose.

from django.contrib import admin  # Import Django's admin module to register models and define admin classes.
from .models import Category, Post, Comment  # Import the models that will be registered in the admin site.

# Register your models here.  # Hint comment retained from original scaffold.

@admin.register(Category)  # Decorator: register the Category model with the admin site using CategoryAdmin.
class CategoryAdmin(admin.ModelAdmin):  # Define admin options for Category by subclassing ModelAdmin.
    """Admin configuration for Category model.

    Controls list display and auto-population of the slug field.
    """  # Class docstring: short description of what this admin class configures.

    list_display = ['name', 'slug']  # Show 'name' and 'slug' columns in the category list view.
    prepopulated_fields = {'slug': ('name',)}  # Auto-fill 'slug' from 'name' when creating a Category.

@admin.register(Post)  # Decorator: register the Post model with the admin site using PostAdmin.
class PostAdmin(admin.ModelAdmin):  # Define admin options for Post by subclassing ModelAdmin.
    """Admin configuration for Post model.

    Configures list display, filtering, search, and slug auto-population.
    """  # Class docstring: explains the main admin features configured here.

    list_display = ['title', 'slug', 'category', 'published', 'created', 'updated']  # Columns shown in post list.
    list_filter = ['published', 'created','updated', 'category']  # Sidebar filters for the post list view.
    list_editable = ['published']  # Allow the 'published' field to be edited directly from the list view.
    prepopulated_fields = {'slug': ('title',)}  # Auto-fill 'slug' from 'title' when creating a Post.
    search_fields = ['title', 'content']  # Enable search by title and content in the admin search box.
    date_hierarchy = 'created'  # Add a date-based drilldown navigation by the 'created' field.

@admin.register(Comment)  # Decorator: register the Comment model with the admin site using CommentAdmin.
class CommentAdmin(admin.ModelAdmin):  # Define admin options for Comment by subclassing ModelAdmin.
    """Admin configuration for Comment model.

    Controls which fields display in the list and which can be edited inline.
    """  # Class docstring: describes what this admin class customizes.

    list_display = ['name', 'email', 'post', 'created', 'active']  # Columns shown in comment list view.
    list_filter = ['active', 'created', 'updated']  # Sidebar filters for comments by active status and timestamps.
    list_editable = ['active']  # Allow toggling comment 'active' status from the list view.
    search_fields = ['name', 'email', 'content']  # Enable search by commenter name, email, and content.