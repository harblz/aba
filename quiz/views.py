from typing import Type
import json
import datetime

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.views.generic import ListView
import random
from django_htmx.http import retarget, trigger_client_event, reswap
from django.template.response import TemplateResponse
from django.apps import apps
from django.utils.safestring import mark_safe
from django.db.models.deletion import Collector

from core.models import Profile
from .models import *
from .forms import TakeQuizForm
from core.decorators import htmx_required


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
    quiz = Quiz.objects.select_related().get(slug=slug)
    questions = []
    areas = []
    if quiz.areas.all().exists():
        areas = quiz.areas.all().values()
    elif not quiz.areas.all():
        areas = quiz.course.content_areas.all().values()
    for area in areas:
        q = BaseQuestion.objects.filter(category=area["slug"]).values("id")
        weight = area["weight"]
        options = []
        for question in q:
            options.append(question["id"])
        questions += random.sample(options, weight)
    return questions


@htmx_required
def _save_progress(request):
    slug = request.headers["code"] + "-" + str(request.headers["number"])
    progress = get_object_or_404(
        QuizProgress, session=request.session.session_key, quiz=slug
    )
    if (answer := request.POST.get("answer")).isdigit():
        progress.key[str(progress.index)]["user_choice"] = answer
    elif answer == "True":
        progress.key[str(progress.index)]["user_choice"] = True
    elif answer == "False":
        progress.key[str(progress.index)]["user_choice"] = False
    progress.index += 1
    progress.save()


@htmx_required
def _continue(request):
    response = None
    if request.GET.get("action") == "check":
        response = _check_answer(request)
    elif request.GET.get("action") == "next":
        _save_progress(request)
        response = _next_question(request)
    elif request.GET.get("action") == "resume":
        response = _next_question(request, resume=True)
    elif request.GET.get("action") == "end":
        _save_progress(request)
        response = _grade_quiz(request)
    return response


@htmx_required
def _next_question(request, **kwargs) -> HttpResponse:
    slug = request.headers["code"] + "-" + str(request.headers["number"])
    progress = get_object_or_404(
        QuizProgress, session=request.session.session_key, quiz=slug
    )
    index = progress.index
    key = progress.key[str(index)]
    question = BaseQuestion.objects.select_related().get(pk=key["question"])
    rel = getattr(question, question.type.model)
    choices = []
    if question.type.model == "multiplechoicequestion":
        choices = [
            (
                answer.id,
                mark_safe(
                    answer.text[:2] + " class='is-inline-block'" + answer.text[2:],
                ),
            )
            for answer in rel.answers.all()
        ]
    elif question.type.model == "truefalsequestion":
        choices = [(True, "True"), (False, "False")]
    form = TakeQuizForm(choices=choices)
    action = None
    if not (_next := str(index + 1)) in progress.key.keys():
        action = "end"
    elif _next in progress.key.keys():
        action = "check"
    context = {
        "form": form,
        "question": question,
        "action": action,
    }
    response = TemplateResponse(
        request,
        "quiz/question_form.html",
        context,
    )
    if request.GET.get("action") == "resume":
        response.context_data["total"] = len(progress.key)
        trigger_client_event(response, "resume", {"index": index + 1}, after="swap")
    return trigger_client_event(response, "reset", after="swap")


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
        count = 0
        for index, question in enumerate(questions):
            q = BaseQuestion.objects.select_related().get(pk=question)
            model = q.type.model
            rel = getattr(q, model)
            answer = None
            if model == "multiplechoicequestion":
                answer = rel.answer_id
            elif model == "truefalsequestion":
                answer = rel.answer
            data[index] = {"question": q.id, "correct": answer}
            count += 1
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
        question = BaseQuestion.objects.select_related().get(
            pk=first_question["question"]
        )
        rel = getattr(question, question.type.model)
        choices = []
        if question.type.model == "multiplechoicequestion":
            choices = [
                (
                    answer.id,
                    mark_safe(
                        answer.text[:2] + " class='is-inline-block'" + answer.text[2:]
                    ),
                )
                for answer in rel.answers.all()
            ]
        elif question.type.model == "truefalsequestion":
            choices = [(True, "True"), (False, "False")]
        form = TakeQuizForm(choices=choices)

        response = TemplateResponse(
            request,
            "quiz/question_form.html",
            {
                "form": form,
                "slug": quiz.slug,
                "question": question,
                "action": "check",
                "total": count,
            },
        )
        return trigger_client_event(response, "reset", after="swap")

    elif isinstance(response, TemplateResponse):
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
def _check_answer(request):
    slug = request.headers["code"] + "-" + str(request.headers["number"])
    progress = get_object_or_404(
        QuizProgress, session=request.session.session_key, quiz=slug
    )
    index = progress.index
    question = progress.key[str(index)]
    # Needs logic to highlight the selected answer in green client side
    if str(request.POST.get("answer")) == str(question["correct"]):
        _save_progress(request)
        response = _next_question(request)
        return response
    elif str(request.POST.get("answer")) != str(question["correct"]):
        q_obj = BaseQuestion.objects.select_related().get(id=question["question"])
        hint = q_obj.hint
        context = {"hint": hint}
        response = TemplateResponse(request, "quiz/hint.html", context)
        reswap(response, "innerHTML")
        retarget(response, "#modals-here")
        return trigger_client_event(response, "show-modal", after="swap")


@htmx_required
def _grade_quiz(request):
    slug = request.headers["code"] + "-" + str(request.headers["number"])
    progress = get_object_or_404(
        QuizProgress, session=request.session.session_key, quiz=slug
    )
    quiz = progress.key
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
        save_data = json.loads(profile.data)
        data = {
            "#correct": n_correct,
            "total": total_q,
            # Time elapsed to go here in ISO8601 Duration format
            # Or save start and end times to be calculated after
            "key": json.loads(progress.key),
        }
        keys = (
            "quizzes",
            request.GET.get("code"),
            str(request.GET.get("number")),
        )
        for key in keys:
            if key not in save_data.keys():
                save_data[key] = {}
                save_data = save_data[key]
            elif key in save_data.keys():
                save_data = save_data[key]
        if (today := datetime.date.today()) not in save_data.keys():
            save_data[datetime.date.today()] = []
        elif today in save_data.keys():
            save_data = save_data[today]
        save_data.append(data)
    return TemplateResponse(request, "quiz/completed.html", context)
