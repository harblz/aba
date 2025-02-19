from django.contrib import admin

from .models import Card, Deck


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    pass


@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    pass
