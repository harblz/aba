from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
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


class Page(models.Model):
    app = models.CharField("App Namespace", max_length=25, null=True, blank=True)
    view = models.CharField("URL Name", max_length=100)
    params = ArrayField(
        models.CharField("Path Parameters", max_length=25, null=True, blank=True),
        null=True,
        blank=True,
    )
    nav = models.BooleanField("Include in Navigation?", default=False)
    root = models.BooleanField("Is Navigation Root?", default=False)
    title = models.CharField(max_length=255, null=True, blank=True)
    subtitle = models.CharField(max_length=255, null=True, blank=True)
    blurb = models.TextField(null=True, blank=True)
    body = CKEditor5Field("Page Body", null=True, blank=True)

    class Meta:
        db_table_comment = "Stores data for Page content and Navbar Links"

    def __str__(self):
        string = f"{self.view}"
        if self.app:
            string = f"{self.app}:{string}"
        if self.params:
            string = f"{string} | {self.params}"
        return string
