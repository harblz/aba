import logging
from typing import Type
from traceback import format_exc
import json

from django.shortcuts import get_object_or_404, render, Http404
from django.http import (
    HttpResponse,
    HttpResponseServerError,
    HttpResponseForbidden,
    HttpResponseBadRequest,
)
from django.views.generic import ListView
import random
from django_htmx.http import retarget, trigger_client_event, reswap
from django.utils import timezone
from django.template.response import TemplateResponse
from django.apps import apps

# from pages.models import Pages
# from learn.models import Course, Lesson, Task, ContentArea
from core.models import Profile
from .models import *
from .forms import TakeQuizForm
from core.decorators import htmx_required
from core.views import handler500


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
    context_object_name = "quizzes"
    template_name = "quiz/index.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(course=self.kwargs["code"])


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
def _save_progress(request):
    progress = get_object_or_404(QuizProgress, session=request.session.session_key)
    progress.key[str(progress.index)]["user_choice"] = request.POST.get("answer")
    progress.index += 1
    progress.save()


@htmx_required
def _next_question(request) -> HttpResponse:
    _save_progress(request)
    progress = get_object_or_404(QuizProgress, session=request.session.session_key)
    index = progress.index
    key = progress.key[str(index)]
    model = apps.get_model("quiz", key["table"])
    question = model.objects.get(pk=key["question"])
    form = TakeQuizForm(question=question)
    if key["table"] == "MultipleChoiceQuestion":
        form.fields["answer"].choices = [
            (answer.id, answer.text) for answer in question.answers.all()
        ]
    elif key["table"] == "TrueFalseQuestion":
        form.fields["answer"].choices = [(True, "True"), (False, "False")]
    return render(
        request, "quiz/question_form.html", {"form": form, "question": question}
    )


@htmx_required
def _start_quiz(request, code, number) -> HttpResponse:
    quiz = Quiz.objects.get(course=code, number=number)
    timed = False
    time = None
    questions = _get_questions(quiz.slug)
    random.shuffle(questions)
    tuple(questions)
    data = {}
    for index, question in enumerate(questions):
        info = question.split(":")
        model = apps.get_model("quiz", info[0])
        obj = model.objects.get(id=info[1])
        index = index
        answer = None
        if info[0] == "MultipleChoiceQuestion":
            answer = obj.answer.id
        elif info[0] == "TrueFalseQuestion":
            answer = obj.answer
        data[index] = {"table": info[0], "question": info[1], "correct": answer}
    if quiz.timed:
        time = quiz.time
        timed = True
    QuizProgress.objects.create(
        user=request.user,
        session=request.session.session_key,
        quiz=quiz.slug,
        index=0,
        timed=timed,
        time=time,
        key=data,
    )

    first_question = data[0]
    model = apps.get_model("quiz", first_question["table"])
    question = model.objects.get(pk=first_question["question"])
    choices = []
    if first_question["table"] == "MultipleChoiceQuestion":
        choices = [(answer.id, answer.text) for answer in question.answers.all()]
    elif first_question["table"] == "TrueFalseQuestion":
        choices = [(True, "True"), (False, "False")]
    form = TakeQuizForm()
    form.fields["answer"].choices = choices

    return render(
        request,
        "quiz/question_form.html",
        {"form": form, "slug": quiz.slug, "question": question},
    )


@htmx_required
def _check_progress(request):
    progress = QuizProgress.objects.get(session=request.session.session_key)
    if progress.exists():
        return
