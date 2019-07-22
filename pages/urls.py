from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('<slug:slug>/', views.pages_base),
]
