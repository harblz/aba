from django.urls import path

from . import views


app_name = "safmeds"

urlpatterns = [
    path("all/", views.card_catalog, name="card_catalog"),
    path("<int:id>/", views.card_detail, name="card_detail"),
    path("", views.browse_decks, name="browse_decks"),
]
