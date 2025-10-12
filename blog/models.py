"""Models for the blog application.

This module defines the data models used by the blog application:

- Category: a simple categorization model for posts.
- Post: blog posts with content, excerpt, image and publication metadata.
- Comment: comments left by visitors on posts.

Each model includes small helper methods (for example
``get_absolute_url``) and sensible Meta options (ordering, indexes)
to improve usability and query performance.
"""

from django.db import models
from django.urls import reverse


class Category(models.Model):
    """Category for grouping blog posts.

    Fields
    - name: Human-readable category name.
    - slug: URL-safe unique identifier used for category pages.
    """

    name = models.CharField(max_length=100)
    # Slug used in URLs; uniqueness prevents duplicate category paths
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        # Order categories alphabetically by name in querysets
        ordering = ['name']
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Return the canonical URL for this category's post list page."""
        return reverse('blog:post_list_by_category', args=[self.slug])


class Post(models.Model):
    """Model representing a blog post.

    Key fields include title, slug (unique URL identifier), content,
    excerpt, image, timestamps, publication flag, and a foreign key to
    Category.
    """

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
    # Short summary used in listings; limited to 300 chars here
    excerpt = models.TextField(max_length=300)
    # Image uploaded to MEDIA_ROOT/blog/
    image = models.ImageField(upload_to='blog/')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # Whether the post is visible to site visitors
    published = models.BooleanField(default=False)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='posts'
    )

    class Meta:
        # Order posts newest-first by default
        ordering = ['-created']
        # Indexes to speed up common queries (ordering by created and
        # filtering by published + ordering by created)
        indexes = [
            models.Index(fields=['-created']),
            models.Index(fields=['-published', '-created']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Return the canonical URL for the post detail page."""
        return reverse('blog:post_detail', args=[self.slug])


class Comment(models.Model):
    """Visitor comments attached to a Post.

    Fields
    - post: FK to the commented post.
    - name, email, content: comment author and body.
    - created, updated: timestamps for moderation and display.
    - active: boolean flag used to hide comments without deleting them.
    """

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        # Order comments by creation time (oldest first)
        ordering = ['created']
        # Index on created helps ordering and time-based queries
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
