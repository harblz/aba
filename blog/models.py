from django.db import models
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field
from datetime import datetime

from taggit.managers import TaggableManager


# Blog Categories
class Category(models.Model):
    category_name = models.CharField(max_length=75, default="Default Category")
    category_description = CKEditor5Field(null=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category_name

    def get_category_name(self):
        return self.category_name

    def get_category_id(self):
        return self.category_id


# Blog Posts
class Post(models.Model):

    tags = TaggableManager()

    author = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=200)
    text = CKEditor5Field()
    pic = models.CharField(max_length=200, null=True, blank=True)
    slug = models.CharField(max_length=200)
    category = models.ForeignKey("blog.Category", on_delete=models.CASCADE, default=0)
    meta = models.CharField(max_length=1000, null=True)
    snippet_size = models.IntegerField(default=150)
    is_pinned = models.BooleanField(null=True, blank=True)

    pic.help_text = "This is the 'splash' picture that will be shown to the user as a header for each post. You can leave it blank. FOR POSTS SERVED UP ON THE SITE, THEY SHOULD START WITH /static/img/"

    is_pinned.help_text = "Pinning a blog post makes it stick to the 'pinned items' bar on the front page of the site. Try not to pin too many posts because it'll look crazy"

    snippet_size.help_text = "The snippet_size determines how much of a text to 'preview' before the post shows the 'read more' button"

    STATUS_CHOICES = (
        ("d", "Draft"),
        ("p", "Published"),
        ("w", "Withdrawn"),
    )

    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    page_views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def publish(self):
        self.published_date = timezone.now()
        self.save()
