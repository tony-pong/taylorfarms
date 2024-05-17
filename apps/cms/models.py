from django.db import models
from django.utils import timezone
from wagtail.snippets.models import register_snippet
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from django.contrib.auth.models import User

# Create your models here.


@register_snippet
class Category(models.Model):
    """A model representing a blog category."""
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class BlogPage(Page):
    """A model representing a blog page."""

    # Blog fields
    author = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    thumbnail = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    category = models.ForeignKey(
        'Category',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    short_content = models.TextField(null=True, blank=True)
    content = RichTextField(null=True, blank=True)
    publishing_date = models.DateTimeField("Publishing Date", default=timezone.now)

    content_panels = Page.content_panels + [
        FieldPanel('author'),
        FieldPanel('thumbnail'),
        FieldPanel('category'),
        FieldPanel('short_content'),
        FieldPanel('content'),
        FieldPanel('publishing_date'),
    ]

    template = "apps/cms/blog_details.html"
