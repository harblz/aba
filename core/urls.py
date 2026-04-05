from django.urls import path

from . import views

urlpatterns = [
    path("account/", views.user_profile, name="user_profile"),
    path("account/edit/", views.edit_profile, name="edit_profile"),
    path("contact/", views.ContactUs.as_view(), name="contact_us"),
]
