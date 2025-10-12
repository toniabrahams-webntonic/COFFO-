"""Simple site-level views for the cafe project.

These views render top-level pages (index, about, coffees, shop) and
provide a search endpoint which aggregates results across multiple
applications (products, blog posts, categories, comments).
"""

from django.shortcuts import render
from django.db.models import Q

# Application models imported for data queries used in the views below.
from cart.models import Product
from blog.models import Post, Category, Comment
from core.models import Review, Contact  # Contact is imported for potential use in contact view (currently unused)


def index(request):
    """Render the home page with recent reviews.

    Retrieves up to three recent reviews and passes them to the
    ``index.html`` template in the ``reviews`` context variable.
    """

    reviews = Review.objects.all().order_by('-date')[:3]
    context = {
        'reviews': reviews,
    }
    return render(request, 'index.html', context)


def about(request):
    """Render the about page."""

    return render(request, 'about.html')


def coffees(request):
    """Render a page describing coffees/offers."""

    return render(request, 'coffees.html')


def shop(request):
    """Render the shop page showing a small selection of products.

    Currently returns up to 6 available products. Templates can use the
    ``products`` context variable to render the product list.
    """

    products = Product.objects.filter(available=True)[:6]  # Show 6 products
    return render(request, 'shop.html', {'products': products})


# def contact(request):
#     return render(request, 'contact.html')


def search(request):
    """Aggregate search across products, posts, categories and comments.

    Query parameter: ?q=<search term>

    The view performs case-insensitive containment searches across a few
    key fields in each model and returns the matching QuerySets in the
    context. If the query is empty, empty lists are returned to the
    template.
    """

    # Read and normalize the query string
    query = request.GET.get('q', '').strip()

    # Default empty results
    product_results = []
    post_results = []
    category_results = []
    comment_results = []

    if query:
        # Search available products by name, description or slug
        product_results = Product.objects.filter(available=True).filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(slug__icontains=query)
        )

        # Search published posts by several textual fields
        post_results = Post.objects.filter(published=True).filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(excerpt__icontains=query) |
            Q(slug__icontains=query)
        )

        # Search categories by name or slug
        category_results = Category.objects.filter(
            Q(name__icontains=query) |
            Q(slug__icontains=query)
        )

        # Search comments by author name, email or content
        comment_results = Comment.objects.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(content__icontains=query)
        )

    context = {
        'query': query,
        'product_results': product_results,
        'post_results': post_results,
        'category_results': category_results,
        'comment_results': comment_results,
    }

    return render(request, 'search.html', context)
