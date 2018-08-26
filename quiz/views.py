from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.views.generic import TemplateView
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.db.models import F
import random

from django.utils import timezone

from .models import Unit, Form, Choice, Question
from pages.models import Pages

def quiz_index(request):
    pages = Pages.objects.order_by('order')
    template_name       = 'quiz/index.html'
    units               = Unit.objects.values("unit_name", "unit_target", "unit_description", "id").all() # Question.objects.values("unit_name").distinct()

    for unit in units:
        unit['count']   = len(Question.objects.values('unit_id').filter(unit_id=unit['id']))
        unit['forms']   = Form.objects.filter(form_unit_id=unit['id'])
        for form in unit['forms']:
            form.count = len(Question.objects.filter(form_id=form.id))

    return render(request, 'quiz/index.html', {
        'units': units,
        'pages': pages
    })

def quiz_view(request, quiz_id, form_id ):
    pages = Pages.objects.order_by('order')
    # get
    if request.method == 'GET':
        quiz_name           = Unit.objects.get(pk=quiz_id)
        form_name           = Form.objects.get(pk=form_id)
        queryset_ids        = Question.objects.filter(unit_id=quiz_id, form_id=form_id).values_list('id', flat=True)
        first_question_id   = random.choice(queryset_ids)
        question            = get_object_or_404(Question, pk=first_question_id)
        unit_name           = quiz_name
        unit_id             = quiz_id
        max_questions       = len(queryset_ids)

        return render(request, 'quiz/quiz.html', {
            'form'              : form_name,
            'form_id'           : form_id,
            'question_ids'      : json.dumps(list(queryset_ids), cls=DjangoJSONEncoder),
            'question'          : question,
            'first_question_id' : first_question_id,
            'unit_name'         : unit_name,
            'unit_id'           : unit_id,
            'total_questions'   : max_questions,
            'pages'             : pages,
        })
        
    # post
    else:
        form_name               = Form.objects.get(pk=form_id).form_name
        attempt                 = request.POST.get('selected_choice')
        attempt_id              = request.POST.get('selected_choice_id')
        prev_question_choice    = Choice.objects.get(id=attempt_id).choice_text
        next_question_id        = request.POST.get('next_question_id')
        quiz_id                 = request.POST.get('unit_id')

        quiz_name               = Unit.objects.get(id=quiz_id)

        Choice.objects.filter(pk=attempt_id).update(votes=F('votes')+1)

        selected_choice     = Choice.objects.get(pk=attempt_id)
        prev_question_id    = selected_choice.question_id 
        prev_question       = Question.objects.get(pk=prev_question_id)
        correct_choice      = Choice.objects.get(question_id=prev_question_id, is_correct=1).choice_text

        try:
            next_question               = Question.objects.get(pk=next_question_id)
            
        except(KeyError, Question.DoesNotExist):
            next_question               = None

        if (next_question == None):
            next_question_choices       = None
            next_question_question_text = None
            next_question_question_hint = None
        else:
            next_question               = Question.objects.get(pk=next_question_id)
            next_question_choices       = Choice.objects.filter(question_id=next_question_id)
            next_question_choices       = [{'id' : item.id, 'choice': item.choice_text} for item in next_question_choices]
            next_question_question_text = next_question.question_text
            next_question_question_hint = next_question.question_hint


        return JsonResponse({
            'form_name'                  : form_name,
            'form_id'               : form_id,
            'unit_name'             : quiz_name.unit_name,
            'question_id'           : next_question_id,
            'question_hint'         : next_question_question_hint,
            'choice_text'           : prev_question_choice,
            'is_correct'            : selected_choice.is_correct,
            'correct_choice_text'   : correct_choice,
            'prev_question_was'     : prev_question.question_text,
            'prev_question_hint'    : prev_question.question_hint,
            'prev_question_choice'  : prev_question_choice,
            'next_question_id'      : next_question_id,
            'next_question_text'    : next_question_question_text,
            'next_question_choices' : next_question_choices
            })