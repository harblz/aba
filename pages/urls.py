from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('<slug:slug>/', views.pages_base),
]
