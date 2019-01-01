from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.views.generic import TemplateView

import json
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict

from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.db.models import F
import random

from django.utils import timezone

from pages.models import Pages
from .models import Unit, Deck, Choice, Flashcard

def fluency_index(request):
    pages = Pages.objects.order_by('order')
    template_name       = 'index.html'
    units               = Unit.objects.values("unit_name", "unit_target", "unit_description", "id").all()

    for unit in units:
        unit['count']   = len(Flashcard.objects.values('unit_id').filter(unit_id=unit['id']))
        unit['decks']   = Deck.objects.filter(deck_unit_id=unit['id'])
        for deck in unit['decks']:
            deck.count = len(Flashcard.objects.filter(deck_id=deck.id))

    return render(request, template_name, {
        'units': units,
        'pages': pages
    })

def tally_vote(request, choice_id):
    choice_id = request.POST.get('choice_id')

    choice = Choice.objects.filter(pk=choice_id).update(votes=F('votes')+1)

    return JsonResponse({
            'choice' : choice,
        })

def fluency_timed_view(request, quiz_id, deck_id ):
    pages = Pages.objects.order_by('order')
    # get
    if request.method == 'GET':
        quiz_name           = Unit.objects.get(pk=quiz_id)
        deck_name           = Deck.objects.get(pk=deck_id).deck_short_name
        deck_timed_duration = Deck.objects.get(pk=deck_id).deck_timed_duration
        flashcard_ids       = Flashcard.objects.filter(unit_id=quiz_id, deck_id=deck_id).values_list('id', flat=True)

        flashcard_set		= list(Flashcard.objects.filter(unit_id=quiz_id, deck_id=deck_id).all())

        for flashcard in flashcard_set:
        	choices = list(Choice.objects.filter(flashcard_id=flashcard.id).values_list('id', 'choice_text', 'is_correct'))

        	flashcard.flashcard_choices = choices

        flashcard_set		= serializers.serialize('json', flashcard_set )

        unit_id             = quiz_id
        max_flashcards      = len(flashcard_ids)

        return render(request, 'fluency_timed.html', {
            'deck'              	: deck_name,
            'deck_id'           	: deck_id,
            'flashcard_ids'         : json.dumps(list(flashcard_ids), cls=DjangoJSONEncoder),
            'deck_timed_duration'   : deck_timed_duration,

            'flashcards'          	: flashcard_set,
            'unit_name'         	: quiz_name,

            'unit_id'           	: unit_id,
            'total_flashcards'   	: max_flashcards,
            'pages'             	: pages,
        })

def fluency_view(request, quiz_id, deck_id ):
    pages = Pages.objects.order_by('order')
    # get
    if request.method == 'GET':
        quiz_name           = Unit.objects.get(pk=quiz_id)
        deck_name           = Deck.objects.get(pk=deck_id).deck_short_name
        flashcard_ids       = Flashcard.objects.filter(unit_id=quiz_id, deck_id=deck_id).values_list('id', flat=True)

        flashcard_set		= list(Flashcard.objects.filter(unit_id=quiz_id, deck_id=deck_id).all())

        for flashcard in flashcard_set:
        	choices = list(Choice.objects.filter(flashcard_id=flashcard.id).values_list('id', 'choice_text', 'is_correct'))

        	flashcard.flashcard_choices = choices

        flashcard_set		= serializers.serialize('json', flashcard_set )

        unit_id             = quiz_id
        max_flashcards      = len(flashcard_ids)

        return render(request, 'fluency.html', {
            'deck'              	: deck_name,
            'deck_id'           	: deck_id,
            'flashcard_ids'      	: json.dumps(list(flashcard_ids), cls=DjangoJSONEncoder),

            'flashcards'          	: flashcard_set,
            'unit_name'         	: quiz_name,

            'unit_id'           	: unit_id,
            'total_flashcards'   	: max_flashcards,
            'pages'             	: pages,
        })