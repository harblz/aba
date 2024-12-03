from typing import Type
from traceback import format_exc

import json, logging

from django.shortcuts import get_object_or_404, render, Http404
from django.http import HttpResponse, HttpResponseServerError, HttpResponseForbidden, HttpResponseBadRequest
from django.views.generic import ListView
import random
from django_htmx.http import retarget, trigger_client_event, reswap
from django.utils import timezone
from django.template.response import TemplateResponse
from django.apps import apps

#from pages.models import Pages
#from learn.models import Course, Lesson, Task, ContentArea
from core.models import Profile
from .models import *
from .forms import TakeQuizForm
from core.decorators import htmx_required
from abarocks.views import handler500

logger = logging.getLogger(__name__)

class QuizIndex(ListView):
    model = Quiz
    context_object_name = "quizzes"
    template_name = "quiz/index.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["page"] = Pages.objects.get(title="Practice Quizzes")
        return context

class IndexByCourse(ListView):
    model = Quiz

    def get_queryset(self):
        queryset = Quiz.objects.filter(self.kwargs["course"])
        return queryset


def get_quiz(request, code, number) -> HttpResponse:
    quiz = Quiz.objects.get(course=code, number=number)
    course = quiz.course

    return render(
        request,
        "quiz/quiz.html",
        {"course": course, "quiz": quiz},
    )


def _get_questions(slug) -> list | Type[Exception]:
    quiz = Quiz.objects.get(slug=slug)
    questions = []
    areas = []
    if quiz.areas.all().exists():
        areas = quiz.areas.all().values()
    elif not quiz.areas.all():
        areas = quiz.course.content_areas.all().values()
    for area in areas:
        tf = TrueFalseQuestion.objects.filter(category=area["slug"]).values("id")
        mc = MultipleChoiceQuestion.objects.filter(category=area["slug"]).values("id")
        weight = area["weight"]
        options = []
        for question in tf:
            options.append(f"TrueFalseQuestion:{question["id"]}")
        for question in mc:
            options.append(f"MultipleChoiceQuestion:{question["id"]}")
        questions += random.sample(options, weight)
    return questions


@htmx_required
def _save_progress(request, slug, index):
    index = str(index)
    request.session["quiz"][slug]["questions"][index]["user_answer"] = (
        request.POST.get("answer")
    )
    index = str(int(index)+1)
    request.session["quiz"][slug]["current_index"] = index


    # noinspection PyTypeChecker
    if request.GET.get("suspend") and request.user.is_authenticated:
        Profile.objects.get(user=request.user).data["quiz"] = request.session["quiz"]
        response = HttpResponse()
        return retarget(response, "")  # TODO: return html for popup and redirect
    elif request.GET.get("suspend"):
        # TODO: need logic for anon users
        pass
    else:
        pass
    """except Exception as e:
        exception = str(e)
        return reswap(handler500(request, exception), "beforeend")"""

"""
class QuizQuestion:
    def __init__(self, question_id, table, user_answer, answer):
        self.question = question_id
        self.table = table
        self.user_answer = user_answer
        self.answer = answer


class UserQuiz:
    def __init__(self, slug, user, index, questions):
        self.slug = slug
        self.user = user
        self.current_index = index
        self.questions = questions
""" 

@htmx_required
def _next_question(request) -> HttpResponse:
    slug = request.POST.get('slug')
    index = request.POST.get('index')
    quiz = request.session["quiz"]
    table = quiz[slug]["questions"]["0"]["table"]
    #quiz_test = UserQuiz(slug, "test user", index, quiz[slug]["questions"])
    if int(index) == quiz[slug]["questions"].__len__()-1:
        return HttpResponse("Quiz Complete. You're awesome!")
    
    _save_progress(request, slug, index)
    quiz[slug]["current_index"] = str(quiz[slug]["current_index"])
    next_index = quiz[slug]["current_index"]
    model = apps.get_model("quiz", table) 
    question = model.objects.get(pk=int(quiz[slug]["questions"][next_index]["question"]))
    form = TakeQuizForm(question=question)
    if table == "MultipleChoiceQuestion":
        form.fields["answer"].choices = [
            (answer.id, answer.text) for answer in question.answers.all()
        ]
    elif table == "TrueFalseQuestion":
        form.fields["answer"].choices = [(True, "True"), (False, "False")]
    json_dump = json.dumps(quiz) #TODO Delete me after figuring out why current_index only iterates once
    return render(request, "quiz/question_form.html", {"form": form, "question": question, "slug": slug, "json": json_dump, "index": next_index})


@htmx_required
def _start_quiz(request, code, number) -> HttpResponse:
    quiz = Quiz.objects.get(course=code, number=number)
    request.session["quiz"] = {}
    request.session["quiz"][quiz.slug] = {}
    request.session["quiz"][quiz.slug]["current_index"] = "0"
    request.session["quiz"][quiz.slug]["questions"] = {}
    questions = _get_questions(quiz.slug)
    random.shuffle(questions)
    tuple(questions)
    for index, question in enumerate(questions):
        info = question.split(":")
        model = apps.get_model("quiz", info[0])
        obj = model.objects.get(id=info[1])
        request.session["quiz"][quiz.slug]["questions"][str(index)] = {}
        request.session["quiz"][quiz.slug]["questions"][str(index)]["question"] = info[
            1
        ]
        if info[0] == "MultipleChoiceQuestion":
            request.session["quiz"][quiz.slug]["questions"][str(index)][
                "answer"
            ] = obj.answer.id
        elif info[0] == "TrueFalseQuestion":
            request.session["quiz"][quiz.slug]["questions"][str(index)][
                "answer"
            ] = obj.answer
        request.session["quiz"][quiz.slug]["questions"][str(index)]["table"] = info[0]
    if quiz.timed:
        time = quiz.time
        request.session["quiz"][quiz.slug]["starttime"] = timezone.now()
        request.session["quiz"][quiz.slug]["timelimit"] = time

    first_question = request.session["quiz"][quiz.slug]["questions"]["0"]
    index = request.session["quiz"][quiz.slug]["current_index"] #TODO delete me after debugging index
    model = apps.get_model("quiz", first_question["table"])
    question = model.objects.get(pk=first_question["question"])
    choices = []
    if first_question["table"] == "MultipleChoiceQuestion":
        choices = [(answer.id, answer.text) for answer in question.answers.all()]
    elif first_question["table"] == "TrueFalseQuestion":
        choices = [(True, "True"), (False, "False")]
    form = TakeQuizForm()
    form.fields["answer"].choices = choices
    json_dump = json.dumps(request.session["quiz"])

    return render(
        request,
        "quiz/question_form.html",
        {"form": form, "slug": quiz.slug, "question": question, "json": json_dump, "index": index},
    )