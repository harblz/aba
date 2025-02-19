from django.shortcuts import render
from django.template.response import TemplateResponse

from .models import Card, Deck


def card_list(request):
    return TemplateResponse(
        request,
        "safmeds/catalog.html",
        {
            "cards": Card.objects.all(),
        },
    )
