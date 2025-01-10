from typing import Type
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
from django.template import Template

# from pages.models import Pages
# from learn.models import Course, Lesson, Task, ContentArea
from core.models import Profile
from .models import *
from .forms import TakeQuizForm
from core.decorators import htmx_required

from django.utils.safestring import mark_safe


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


def show_quiz(request, code, number) -> HttpResponse:
    quiz_obj = Quiz.objects.get(course=code, number=number)
    course = quiz_obj.course
    request.session.set_test_cookie()
    headers = {"code": "RBT", "number": 1}

    return render(
        request,
        "quiz/quiz.html",
        {"course": course, "quiz": quiz_obj, "headers": headers},
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
# Add ", code, number" when client-side storage figured out
def _save_progress(request):
    slug = request.GET.get("code") + "-" + str(request.GET.get("number"))
    progress = get_object_or_404(
        QuizProgress, session=request.session.session_key, slug=slug
    )
    progress.key[str(progress.index)]["user_choice"] = request.POST.get("answer")
    progress.index += 1
    progress.save()


@htmx_required
# Add ", code, number" when client-side storage figured out
def _continue(request, **kwargs) -> HttpResponse:
    if request.GET.get("continue") == "next" or "next" in kwargs:
        _save_progress(request)
    elif request.GET.get("continue") == "resume":
        pass
    slug = request.GET.get("code") + "-" + str(request.GET.get("number"))
    progress = get_object_or_404(
        QuizProgress, session=request.session.session_key, slug=slug
    )
    index = progress.index
    key = progress.key[str(index)]
    model = apps.get_model("quiz", key["table"])
    question = model.objects.get(pk=key["question"])
    choices = []
    if key["table"] == "MultipleChoiceQuestion":
        choices = [
            (
                answer.id,
                mark_safe(
                    answer.text[:2] + " class='is-inline-block'" + answer.text[2:]
                ),
            )
            for answer in question.answers.all()
        ]
    elif key["table"] == "TrueFalseQuestion":
        choices = [(True, "True"), (False, "False")]
    form = TakeQuizForm(choices=choices)
    response = TemplateResponse(
        request, "quiz/question_form.html", {"form": form, "question": question}
    )
    return trigger_client_event(response, "reset", after="swap")
    # Add ", code, number" when client-side storage figured out


@htmx_required
def _start(request, code, number) -> HttpResponse:
    quiz = Quiz.objects.get(course=code, number=number)
    if (response := _check_progress(request, code, number)) is None or bool(
        request.GET.get("confirm")
    ) == True:
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
        QuizProgress.objects.update_or_create(
            user=request.user if request.user.is_authenticated else None,
            session=request.session.session_key,
            quiz=quiz.slug,
            defaults={
                "index": 0,
                "timed": timed,
                "time": time,
                "key": data,
            },
        )

        first_question = data[0]
        model = apps.get_model("quiz", first_question["table"])
        question = model.objects.get(pk=first_question["question"])
        choices = []
        if first_question["table"] == "MultipleChoiceQuestion":
            choices = [
                (answer.id, mark_safe(answer.text)) for answer in question.answers.all()
            ]
            choices = [
                (
                    answer.id,
                    mark_safe(
                        answer.text[:2] + " class='is-inline-block'" + answer.text[2:]
                    ),
                )
                for answer in question.answers.all()
            ]
        elif first_question["table"] == "TrueFalseQuestion":
            choices = [(True, "True"), (False, "False")]
        form = TakeQuizForm(choices=choices)

        response = TemplateResponse(
            request,
            "quiz/question_form.html",
            {"form": form, "slug": quiz.slug, "question": question},
        )
        return trigger_client_event(response, "reset", after="swap")

    elif type(response) is TemplateResponse:
        reswap(response, "innerHTML")
        retarget(response, "#modals-here")
        return trigger_client_event(response, "show-modal", after="swap")


@htmx_required
def _check_progress(request, code, number):
    slug = code + "-" + str(number)
    progress = QuizProgress.objects.filter(
        session=request.session.session_key, quiz=slug
    )
    if progress.exists():
        context = {"quiz": Quiz.objects.get(slug=slug)}
        response = TemplateResponse(request, "quiz/confirmation.html", context)
        return response
    elif not progress.exists():
        return None


@htmx_required
# Add ", code, number" when client-side storage figured out
def _check_answer(request):
    slug = request.GET.get("code") + "-" + str(request.GET.get("number"))
    progress = get_object_or_404(
        QuizProgress, session=request.session.session_key, slug=slug
    )
    index = progress.index
    question = progress.key[str(index)]
    if request.POST.get("answer") == str(question["correct"]):
        # Needs logic to highlight the selected answer in green client side
        response = _continue(request, next=True)
        return response
    elif request.POST.get("answer") != str(question["correct"]):
        model = apps.get_model("quiz", question["table"])
        q_obj = model.objects.get(id=question["question"])
        hint = q_obj.hint
        context = {"hint": hint}
        response = TemplateResponse(request, "quiz/hint.html", context)
        reswap(response, "innerHTML")
        retarget(response, "#modals-here")
        return trigger_client_event(response, "show-modal", after="swap")


@htmx_required
def _grade_quiz(request):
    slug = request.GET.get("code") + "-" + str(request.GET.get("number"))
    progress = get_object_or_404(
        QuizProgress, session=request.session.session_key, slug=slug
    )
    quiz = json.loads(progress.key)
    total_q = 0
    total_q = sum(1 for key in quiz.keys())
    n_correct = 0
    for key, value in quiz.items():
        correct = value["correct"]
        answer = value["user_choice"]
        if correct == answer:
            n_correct += 1
    percent = (n_correct / total_q) * 100
    context = {
        "correct": n_correct,
        "total": total_q,
        "percent": percent,
        "code": request.GET.get("code"),
        "number": request.GET.get("number"),
    }
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        save_data = profile.data
        data = {}
        if "quizzes" not in data.keys:
            save_data["quizzes"] = {}
        save_data = save_data["quizzes"]
        if request.GET.get("code") not in save_data.keys():
            save_data[request.GET.get("code")] = {}
        save_data = save_data[request.GET.get("code")]
        if str(request.GET.get("number")) not in save_data.keys():
            save_data[request.GET.get("number")] = {}
        save_data = save_data[request.GET.get("number")]

    return TemplateResponse(request, "quiz/completed.html", context)
