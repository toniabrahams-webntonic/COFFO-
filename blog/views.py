"""Views for the blog application with per-line explanations.

This module contains two view functions: `post_list` which shows a
paginated list of published posts (optionally filtered by category), and
`post_detail` which displays a single post with its comments and a form to
submit new comments.
"""

from django.shortcuts import render, get_object_or_404  # Helpers for rendering templates and fetching objects or returning 404.
from django.core.paginator import Paginator  # Paginator utility for splitting querysets into pages.
from .models import Post, Category, Comment  # Import local models used by the views.
from .forms import CommentForm  # Import the form used to submit comments.


def post_list(request, category_slug=None):
    """Render a paginated list of published posts, optionally filtered.

    Args:
        request: HttpRequest object provided by Django.
        category_slug: Optional slug to filter posts by category.

    Returns:
        HttpResponse rendering the 'blog/post_list.html' template with
        context variables for the category, list of categories, and the page
        object containing posts for the current page.
    """
    category = None  # Initialize category variable when no slug provided.
    categories = Category.objects.all()  # Fetch all categories for sidebar/navigation.
    posts = Post.objects.filter(published=True)  # Start with only published posts.

    if category_slug:
        # If a category slug is provided, resolve it or return 404.
        category = get_object_or_404(Category, slug=category_slug)
        posts = posts.filter(category=category)  # Narrow posts to the chosen category.

    paginator = Paginator(posts, 6)  # Paginate the posts: 6 posts per page.
    page_number = request.GET.get('page')  # Read current page number from query params.
    page_obj = paginator.get_page(page_number)  # Get the page object for rendering.

    return render(request, 'blog/post_list.html', {
        'category': category,  # The currently selected category (or None).
        'categories': categories,  # All categories for the template.
        'page_obj': page_obj,  # Page object with posts for the template.
    })


def post_detail(request, slug):
    """Render a detail view for a single published post and handle comments.

    Args:
        request: HttpRequest object.
        slug: Slug of the post to display.

    Returns:
        HttpResponse rendering the 'blog/post_detail.html' template with
        the post, its active comments, a new_comment placeholder, and the
        comment_form instance.
    """
    post = get_object_or_404(Post, slug=slug, published=True)  # Fetch the post or 404.
    comments = post.comments.filter(active=True)  # Only include active (approved) comments.
    new_comment = None  # Placeholder for a newly created comment instance.

    if request.method == 'POST':
        # If the request is a POST, the user submitted the comment form.
        comment_form = CommentForm(data=request.POST)  # Bind form to POST data.
        if comment_form.is_valid():
            # Save the form but don't commit to add the post relationship.
            new_comment = comment_form.save(commit=False)
            new_comment.post = post  # Associate the new comment with the current post.
            new_comment.save()  # Persist the new comment to the database.
    else:
        comment_form = CommentForm()  # Empty form for GET requests.

    return render(request, 'blog/post_detail.html', {
        'post': post,  # The post being viewed.
        'comments': comments,  # Active comments to display.
        'new_comment': new_comment,  # Newly created comment or None.
        'comment_form': comment_form,  # Form to submit comments in the template.
    })