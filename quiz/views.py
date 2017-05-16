from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.views.generic import TemplateView
import json
from django.http import HttpResponse
from django.http import JsonResponse

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

def quiz_view(request, quiz_name, question_id ):
    question  = get_object_or_404(Question, pk=question_id)
    unit_name = quiz_name
    questions = Question.objects.filter(
        unit_name=unit_name
    ).order_by('-id')

    return render(request, 'quiz/quiz.html', {
        'question': question,
        'unit_name': unit_name,
        'questions': questions,
    })

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
