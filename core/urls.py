from django.urls import path, include, re_path

from . import views
from core import views as core

urlpatterns = [
    path("account/", views.user_profile, name="user_profile"),
    path("account/edit/", views.edit_profile, name="edit_profile"),
]
