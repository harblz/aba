from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    data = models.JSONField(default=dict)

    class Meta:
        db_table_comment = (
            "Profiles for learner tracking linked to django.contrib.auth.user"
        )

    def __str__(self):
        return self.user


class NavLink(models.Model):
    path = models.URLField()


class PageContent(models.Model):
    page = models.SlugField(max_length=200, unique=True, primary_key=True)
    heading = models.CharField(max_length=255, null=True, blank=True)
    subheading = models.CharField(max_length=255, null=True, blank=True)
    body = CKEditor5Field("Page Body", null=True, blank=True)
