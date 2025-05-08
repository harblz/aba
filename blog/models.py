from django.db import models
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field
from datetime import datetime

from taggit.managers import TaggableManager


# Blog Categories
class Category(models.Model):
    slug = models.SlugField(max_length=50, unique=True)
    category = models.CharField(max_length=50, default="Default Category")
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category

    def save(self, *args, **kwargs):
        self.slug = self.slug.lower()
        super(Category, self).save()

    def get_category(self):
        return self.category


class Post(models.Model):
    slug = models.SlugField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=250, null=True)
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    tags = TaggableManager()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=0)
    body = CKEditor5Field()
    pinned = models.BooleanField(null=True, blank=True)
    draft = models.BooleanField(default=False, blank=True)
    published = models.BooleanField(default=False, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def publish(self):
        self.published_date = timezone.now()
        self.save()
