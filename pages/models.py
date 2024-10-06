from django.db import models
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field
from datetime import datetime


# Create your models here.
class Pages(models.Model):
    author = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    text = CKEditor5Field()
    order = models.IntegerField()  # TODO: Remove
    icon = models.CharField(max_length=50)
    STATUS_CHOICES = (
        ("d", "Draft"),
        ("p", "Published"),
        ("w", "Withdrawn"),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    page_views = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Site Pages"

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
