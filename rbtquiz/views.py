from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render


from .models import QuizChoice, QuizQuestion


def index(request):
    latest_question_list = QuizQuestion.objects.order_by('-pub_date')[:5]
    template = loader.get_template('rbtquiz/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))

def detail(request, question_id):
    question = get_object_or_404(QuizQuestion, pk=question_id)
    return render(request, 'rbtquiz/detail.html', {'question': question})

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    question = get_object_or_404(QuizQuestion, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, QuizChoice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'rbtquiz/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('rbtquiz:results', args=(question.id,)))
