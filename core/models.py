from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django_ckeditor_5.fields import CKEditor5Field
from django.core.exceptions import ObjectDoesNotExist


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    data = models.JSONField(default=dict)

    class Meta:
        db_table_comment = (
            "Profiles for learner tracking linked to django.contrib.auth.user"
        )

    def __str__(self):
        return self.user.username


class Page(models.Model):
    app = models.CharField(max_length=25, null=True, blank=True)
    view = models.CharField("URL Name", max_length=100)
    params = ArrayField(
        models.CharField("Path Parameters", max_length=25, null=True, blank=True),
        null=True,
        blank=True,
    )
    nav = models.BooleanField("Include in Navigation?", default=False)
    title = models.CharField(max_length=255, null=True, blank=True)
    subtitle = models.CharField(max_length=255, null=True, blank=True)
    blurb = models.TextField(null=True, blank=True)
    body = CKEditor5Field("Page Body", null=True, blank=True)

    class Meta:
        db_table_comment = "Stores data for Page content and Navbar Links"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Page, self).save(*args, **kwargs)
        if self.nav:
            NavLink.objects.update_or_create(page=self, create_defaults={"root": False})
        elif not self.nav:
            try:
                NavLink.objects.get(page=self).delete()
            except ObjectDoesNotExist:
                pass

    def url_string(self):
        view_string = self.view
        if self.app:
            view_string = f"{self.app}:{view_string}"
        return view_string


class NavLink(models.Model):
    page = models.OneToOneField(Page, on_delete=models.CASCADE, unique=True)
    label = models.CharField(max_length=255, null=True, blank=True)
    root = models.BooleanField("Is Navigation Root?", default=False)
    has_children = models.BooleanField("Has child pages?", default=False)
    root_pos = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.page.__str__()


class View(models.Model):
    url = models.URLField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(null=True, blank=True)


class SupportTicket(models.Model):
    MESSAGE_TYPES = {
        "TECH": "Tech Support",
        "FEAT": "Feature Request",
    }
    type = models.CharField(max_length=5)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    closed = models.BooleanField(default=False)

    def __str__(self):
        return self.message


class SupportResponse(models.Model):
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    message = models.TextField(max_length=255)

    def __str__(self):
        return self.message
