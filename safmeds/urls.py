from django.urls import path

from . import views


app_name = "safmeds"

urlpatterns = [
    path("all/", views.card_list, name="card_list"),
]
