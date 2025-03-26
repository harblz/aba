from django.shortcuts import render
from django.template.response import TemplateResponse

from .models import Card, Deck


def card_catalog(request):
    return TemplateResponse(
        request,
        "safmeds/deck.html",
        {
            "cards": Card.objects.all(),
        },
    )


def deck_editor(request):
    pass


def card_detail(request, id):
    return TemplateResponse(
        request, "safmeds/detail.html", {"card": Card.objects.get(id=id), "id": id}
    )


def browse_decks(request):
    decks = Deck.objects.all()
    return render(request, "safmeds/main.html", context={"decks": decks})
