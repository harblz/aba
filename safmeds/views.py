from django.http import HttpResponse
from django.shortcuts import render
from django.template.response import TemplateResponse
from django_htmx.http import trigger_client_event
import json

from .models import Card, Deck, Result


def card_catalog(request):
    return TemplateResponse(
        request,
        "safmeds/catalog.html",
        {
            "cards": Card.objects.all(),
        },
    )


def deck_editor(request):
    pass


def card_detail(request, id):
    return TemplateResponse(
        request, "safmeds/play_card.html", {"card": Card.objects.get(id=id), "id": id}
    )


def browse_decks(request):
    decks = Deck.objects.all()
    return render(request, "safmeds/main.html", context={"decks": decks})


def view_deck(request, slug):
    deck = Deck.objects.get(slug=slug)
    if request.htmx:
        response = TemplateResponse(
            request, "safmeds/deck_preview.html", context={"deck": deck}
        )
        return trigger_client_event(response, "show-modal", after="swap")
    else:
        return TemplateResponse(request, "safmeds/deck.html", context={"deck": deck})


def _play(request, slug):
    deck = Deck.objects.get(slug=slug)
    data = list(deck.cards.all().values())
    return TemplateResponse(
        request,
        "safmeds/play_card.html",
        context={"deck": deck, "data": json.dumps(data)},
    )


def _results(request, slug):
    correct = int(request.GET.get("correct"))
    incorrect = int(request.GET.get("incorrect"))
    total = int(request.GET.get("total"))
    score = (float(correct) / float(total)) * 100
    context = {
        "slug": slug,
        "name": request.GET.get("name"),
        "correct": correct,
        "incorrect": incorrect,
        "total": total,
        "score": score,
    }
    if request.user.is_authenticated:
        deck = Deck.objects.get(slug=slug)
        Result.objects.create(
            user=request.user,
            deck=deck,
            correct=correct,
            incorrect=incorrect,
            score=score,
        )
    return TemplateResponse(request, "safmeds/results.html", context)
