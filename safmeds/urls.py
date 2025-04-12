from django.urls import path

from . import views


app_name = "safmeds"

urlpatterns = [
    path("all/", views.card_catalog, name="card-catalog"),
    path("card/<int:id>/", views.card_detail, name="card-detail"),
    path("<str:slug>/play", views._play, name="play-deck"),
    path("<str:slug>/results/", views._results, name="results"),
    path("<str:slug>/", views.view_deck, name="view-deck"),
    path("", views.browse_decks, name="browse-decks"),
]
