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
from datetime import datetime    

from .models import Unit, Form, Choice, Question, Task, QuizScore
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


def quiz_question_inspector(request, question_id):

    pages = Pages.objects.order_by('order')
    question  = get_object_or_404(Question, pk=question_id)

    correct_choice = list(Choice.objects.filter(question_id=question.id, is_correct=True).values_list('id', 'choice_text', 'is_correct'))

    return render(request, 'quiz/quiz_question_inspector.html', {
        'question'          : question,
        'correct_choice'    : correct_choice,
        'pages'             : pages,
    })


def submit_score_report(request):
    #send_mail('Subject here','Here is the message.','alex@behaviorist.tech',['alex@behaviorist.tech'],fail_silently=False,)
    score           = request.POST.get("quiz_score")

    unit_id         = request.POST.get("unit_id")
    unit            = Unit.objects.get(pk=unit_id)

    form_id         = request.POST.get("form_id")
    form            = Form.objects.get(pk=form_id)

    results         = QuizScore(score=score, unit_id=unit, form_id=form, date=datetime.now())
    results.save()

    return JsonResponse({
            'unit_id'   : unit_id,
            'form_id'   : form_id,
            'score'     : score,
        })


def quiz_view(request, quiz_id, form_id ):
    pages = Pages.objects.order_by('order')
    # get
    if request.method == 'GET':
        quiz_name           = Unit.objects.get(pk=quiz_id)
        form_name           = Form.objects.get(pk=form_id).form_short_name
        queryset_ids        = Question.objects.filter(unit_id=quiz_id, form_id=form_id).values_list('id', flat=True)
        first_question_id   = random.choice(queryset_ids)
        question            = get_object_or_404(Question, pk=first_question_id)
        unit_name           = quiz_name
        unit_id             = quiz_id
        task_item           = Task.objects.get(pk=question.task_list_item_id).task_name
        max_questions       = len(queryset_ids)

        return render(request, 'quiz/quiz.html', {
            'form'              : form_name,
            'form_id'           : form_id,
            'task_item'         : task_item,
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
        form_short_name         = Form.objects.get(pk=form_id).form_short_name
        next_question_id        = request.POST.get('next_question_id')
        prev_question_id        = request.POST.get('prev_question_id')
        quiz_id                 = request.POST.get('unit_id')

        quiz_name               = Unit.objects.get(id=quiz_id)

        #Choice.objects.filter(pk=attempt_id).update(votes=F('votes')+1)

        #1 at the end of the test, don't worry if there is no next question
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
            next_question               = list(Question.objects.filter(pk=next_question_id).values_list('id', 'question_text', 'question_hint', 'task_list_item_id'))

    
        #2 at the start of the test, don't worry if there is no prev question
        try:
            prev_question       = Question.objects.get(pk=prev_question_id)

        except(KeyError, Question.DoesNotExist):
            prev_question = None

        if ( prev_question == None):
            choices             = list(Choice.objects.filter(question_id=next_question_id).values_list('id', 'choice_text', 'is_correct'))
            prev_question       = None
            prev_correct_choice = None
            prev_question_hint   = None

        else:
            choices             = list(Choice.objects.filter(question_id=next_question_id).values_list('id', 'choice_text', 'is_correct'))
            prev_question       = list(Question.objects.filter(pk=prev_question_id).values_list('id', 'question_text', 'question_hint', 'task_list_item_id'))
            prev_correct_choice = list(Choice.objects.filter(question_id=prev_question_id, is_correct=True).values_list('choice_text'))
            prev_question_hint   = prev_question[0][2]

        task_item     = Task.objects.get(pk=next_question[0][3]).task_name

        return JsonResponse({
            'form'                  : form_name,
            'form_id'               : form_id,
            'form_short_name'       : form_short_name,
            'unit_name'             : quiz_name.unit_name,
            'choices'               : choices,
            'next_question'         : next_question,
            'prev_question'         : prev_question,
            'prev_question_hint'    : prev_question_hint,
            'prev_correct_choice'   : prev_correct_choice,
            'task_item'             : task_item
            })