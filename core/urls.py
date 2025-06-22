from django.urls import path, include, re_path

from . import views
from core import views as core

urlpatterns = [
    path("accounts/signup/", core.SignUpView.as_view(), name="signup"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("account/", views.user_profile, name="user_profile"),
]
