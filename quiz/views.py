from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.views.generic import TemplateView
import json
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers

from django.utils import timezone

from .models import Choice, Question

class IndexView(generic.ListView):
    template_name = 'quiz/index.html'
    context_object_name = 'quizes_available'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]
        """
        return Question.objects.values("unit_name").distinct()

class QuizView(generic.ListView):
    template_name = 'quiz/quiz.html'
    context_object_name = 'quiz'

    def get_queryset(request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        return question

def quiz_view(request, quiz_name ):
    if request.method == 'GET':
        first_question_id = Question.objects.filter(unit_name=quiz_name).first().id
        question  = get_object_or_404(Question, pk=first_question_id)
        unit_name = quiz_name
        questions = Question.objects.filter(
            unit_name=unit_name
        ).order_by('-id')

        return render(request, 'quiz/quiz.html', {
            'question'  : question,
            'unit_name' : unit_name,
            'questions' : questions,
        })
    else:
        attempt          = request.POST.get('selected_choice')
        attempt_id       = request.POST.get('selected_choice_id')
        selected_choice  = Choice.objects.get(pk=attempt_id)
        question_id      = selected_choice.question_id
        question         = get_object_or_404(Question, pk=question_id)
        question_set     = Question.objects.filter(unit_name=quiz_name).all()
        last_question_id = Question.objects.filter(unit_name=question.unit_name).all().latest('id').id
        question_hint    = question.question_hint
        continue_quiz    = False

        if question_id == last_question_id:
            x = question_id
        else:
            for index, q in enumerate(question_set):
                if question_id == q.id:
                    x = question_set[index + 1].id
                    break
                else:
                    x = question_id

        next_question_id      = x
        next_question         = Question.objects.filter(pk=x).get()
        next_question_choices = Choice.objects.filter(question_id=next_question)
        next_choices          = [{'id' : item.id, 'choice': item.choice_text} for item in next_question_choices]

        if question.id < last_question_id:
            continue_quiz = True
        else:
            continue_quiz = False


        return JsonResponse({
            'unit_name'     : question.unit_name,
            'question_id'   : question.id,
            'question_hint' : question.question_hint,
            'choice_text'   : attempt,
            'is_correct'    : selected_choice.is_correct,
            'last_id'       : last_question_id,
            'continue_quiz' : continue_quiz,
            'next_question_id' : next_question_id,
            'next_question_text' : next_question.question_text,
            'next_question_choices' : next_choices
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
