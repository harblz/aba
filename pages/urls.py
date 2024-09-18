from django.urls import include, re_path
from django.urls import path
from . import views

urlpatterns = [
    path("<slug:slug>/", views.pages_base),
]
