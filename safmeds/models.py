from django.db import models

from learn.models import Course


class Card(models.Model):
    back = models.CharField(max_length=50)
    front = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["back", "front"], name="unique_cards")
        ]


class Deck(models.Model):
    slug = models.SlugField(max_length=50, unique=True, primary_key=True)
    name = models.CharField(max_length=50)
    subject = models.ForeignKey(Course, on_delete=models.CASCADE)
    deck = models.ManyToManyField(Card, related_name="decks")
