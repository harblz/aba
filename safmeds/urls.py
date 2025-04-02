from django.urls import path

from . import views


app_name = "safmeds"

urlpatterns = [
    path("all/", views.card_catalog, name="card_catalog"),
    path("<int:id>/", views.card_detail, name="card_detail"),
    path("<str:slug>/", views.view_deck, name="view_deck"),
    path("<str:slug>/play", views.play, name="play_deck"),
    path("", views.browse_decks, name="browse_decks"),
]
