from django.shortcuts import render
from django.template.response import TemplateResponse

from .models import Card, Deck


def card_catalog(request):
    return TemplateResponse(
        request,
        "safmeds/catalog.html",
        {
            "cards": Card.objects.all(),
        },
    )


def card_detail(request, id):
    return TemplateResponse(
        request, "safmeds/detail.html", {"card": Card.objects.get(id=id)}
    )
