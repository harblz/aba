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

from .models import Choice, Question

def quiz_index(request):
    template_name       = 'quiz/index.html'
    unit_names          = Question.objects.values("unit_name").distinct()

    for unit in unit_names:
        unit['count']    = len(Question.objects.values('unit_name').filter(unit_name=unit['unit_name']))

    return render(request, 'quiz/index.html', {
        'unit_names'        : unit_names,
    })

def quiz_view(request, quiz_name ):
    if request.method == 'GET':
        queryset_ids        = Question.objects.filter(unit_name=quiz_name).values_list('id', flat=True)
        first_question_id   = random.choice(queryset_ids)
        question            = get_object_or_404(Question, pk=first_question_id)
        unit_name           = quiz_name
        max_questions       = len(queryset_ids)

        return render(request, 'quiz/quiz.html', {
            'question_ids'      : json.dumps(list(queryset_ids), cls=DjangoJSONEncoder),
            'question'          : question,
            'first_question_id' : first_question_id,
            'unit_name'         : unit_name,
            'total_questions'   : max_questions,
        })
    # post
    else:
        attempt             = request.POST.get('selected_choice')
        attempt_id          = request.POST.get('selected_choice_id')
        next_question_id    = request.POST.get('next_question_id')

        Choice.objects.filter(pk=attempt_id).update(votes=F('votes')+1)

        selected_choice     = Choice.objects.get(pk=attempt_id)
        prev_question_id    = selected_choice.question_id
        prev_question       = Question.objects.get(pk=prev_question_id)
        correct_choice      = Choice.objects.get(question_id=prev_question_id, is_correct=1).choice_text

        try:
            next_question               = Question.objects.get(pk=next_question_id)
        except(KeyError, Question.DoesNotExist):
            next_question               = None

        #next_question               = Question.objects.get(pk=next_question_id)
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
            'unit_name'             : quiz_name,
            'question_id'           : next_question_id,
            'question_hint'         : next_question_question_hint,
            'choice_text'           : attempt,
            'is_correct'            : selected_choice.is_correct,
            'correct_choice_text'   : correct_choice,
            'prev_question_was'     : prev_question.question_text,
            'prev_question_hint'    : prev_question.question_hint,
            'prev_question_choice'  : attempt,
            'next_question_id'      : next_question_id,
            'next_question_text'    : next_question_question_text,
            'next_question_choices' : next_question_choices
            })

def home(request):
    if request.method == 'POST':
        post_text = request.POST.get('the_post')
        response_data = {}

        return JsonResponse({'foo':'bar post'})

    else:
        return JsonResponse({'foo':'bar get'})

def create_post(request, quiz_name, question_id):
    if request.method == 'POST':
        post_text = request.POST.get('the_post')
        response_data = {}

        return JsonResponse({'foo':'bar'})

    else:
        return JsonResponse({'foo':'bar'})



class DetailView(TemplateView):
    template_name = 'quiz/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'quiz/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'quiz/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('quiz:results', args=(question.id,)))
