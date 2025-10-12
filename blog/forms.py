"""Forms for the blog application.

This module defines form classes used by the blog app. Currently it
provides ``CommentForm``, a ModelForm for creating and validating
comments submitted by site visitors.
"""

from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    """Form for creating a Comment instance.

    This form is based on the :class:`blog.models.Comment` model and
    exposes the name, email and content fields. The form customizes the
    default widgets to include Bootstrap-compatible CSS classes and
    placeholders to improve UX when rendered in templates.

    Usage:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            # attach additional data before saving if needed
            comment.save()
    """

    class Meta:
        # The model this ModelForm creates/edits
        model = Comment

        # Fields from the model to include in the form (order preserved)
        fields = ['name', 'email', 'content']

        # Customize the HTML widgets used for each field. These attrs
        # include Bootstrap classes and placeholders used by templates.
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Your Name'}
            ),
            'email': forms.EmailInput(
                attrs={'class': 'form-control', 'placeholder': 'Your Email'}
            ),
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Your Comment',
                }
            ),
        }
