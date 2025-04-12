from django.db import models
from django.template.defaultfilters import slugify

from learn.models import Course


class Card(models.Model):
    back = models.CharField(max_length=50)
    front = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["back", "front"], name="unique_cards")
        ]

    def __str__(self):
        return self.front


class Deck(models.Model):
    slug = models.SlugField(max_length=50, unique=True, primary_key=True)
    name = models.CharField(max_length=50)
    subject = models.ForeignKey(Course, on_delete=models.CASCADE)
    cards = models.ManyToManyField(Card, related_name="decks")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug and self._state.adding:
            self.slug = slugify(self.name)
            super(Deck, self).save(*args, **kwargs)
