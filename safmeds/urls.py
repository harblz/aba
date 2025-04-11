from django.urls import path

from . import views


app_name = "safmeds"

urlpatterns = [
    path("results/", views.results, name="results"),
    path("all/", views.card_catalog, name="card_catalog"),
    path("card/<int:id>/", views.card_detail, name="card_detail"),
    path("<str:slug>/play", views.play, name="play_deck"),
    path("<str:slug>/", views.view_deck, name="view_deck"),
    path("", views.browse_decks, name="browse_decks"),
]
