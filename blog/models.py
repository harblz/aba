from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from datetime import datetime

# Blog Categories
class Category(models.Model):
    category_name           = models.CharField(max_length=75, default='Default Category')
    category_description    = RichTextField(null=True)

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
    CATEGORY_CHOICES = (
        ('green','GREEN'),
        ('blue', 'BLUE'),
        ('red','RED'),
        ('orange','ORANGE'),
        ('black','BLACK'),
    )

    author           = models.ForeignKey('auth.User', on_delete=models.CASCADE,)
    title            = models.CharField(max_length=200)
    text             = RichTextField()
    pic              = models.CharField(max_length=200, null=True, blank=True)
    slug             = models.CharField(max_length=200)
    category         = models.CharField(max_length=75, choices=CATEGORY_CHOICES, default='Default')
    meta             = models.CharField(max_length=1000, null=True)
    snippet_size     = models.IntegerField(default=150)
    is_pinned        = models.NullBooleanField(default=False)

    pic.help_text           = "This is the 'splash' picture that will be shown to the user as a header for each post. You can leave it blank."

    is_pinned.help_text     = "Pinning a blog post makes it stick to the 'pinned items' bar on the front page of the site. Try not to pin too many posts because it'll look crazy"

    snippet_size.help_text  = "The snippet_size determines how much of a text to 'preview' before the post shows the 'read more' button"

    STATUS_CHOICES = (
        ('d', 'Draft'),
        ('p', 'Published'),
        ('w', 'Withdrawn'),
    )

    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)
    page_views = models.IntegerField(default=0)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
