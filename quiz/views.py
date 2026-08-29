import random
from typing import Type

from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.response import TemplateResponse
from django.utils.safestring import mark_safe
from django_htmx.http import retarget, trigger_client_event, reswap

from core.decorators import htmx_required
from learn.models import Course
from .forms import TakeQuizForm
from .models import *


def quiz_index(request):
    quizzes = Quiz.objects.all().order_by("course_id")
    courses = Course.objects.all().order_by("code")
    return TemplateResponse(
        request, "quiz/index.html", {"quizzes": quizzes, "courses": courses}
    )


def quizzes_by_course(request, code):
    quizzes = Quiz.objects.filter(course_id=code)
    return TemplateResponse(request, "quiz/index.html", {"quizzes": quizzes})


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
    try:
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
    except Exception as e:
        return e


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
    rel = getattr(question, str(question.type.model))
    choices = []
    if question.type.model == "multiplechoicequestion":
        choices = [
            (
                answer.id,
                mark_safe(answer.text),
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
def _start(request, code, number):
    quiz = quiz = get_object_or_404(Quiz, course=code, number=number)
    if (response := _check_progress(request, code, number)) is None or bool(
        request.GET.get("confirm")
    ):
        timed = False
        time = None
        questions = _get_questions(quiz.slug)
        random.shuffle(questions)
        questions = tuple(questions)
        data = {}
        count = 0
        for index, question in enumerate(questions):
            q = BaseQuestion.objects.select_related().get(pk=question)
            model = str(q.type.model)
            rel = getattr(q, model)
            answer = None
            if model == "multiplechoicequestion":
                answer = None
                for answer in rel.answers.all():
                    if answer.is_correct:
                        answer = answer.id
                        break
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
        rel = getattr(question, str(question.type.model))
        choices = []
        if question.type.model == "multiplechoicequestion":
            choices = [
                (
                    answer.id,
                    mark_safe(answer.text),
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

    else:
        reswap(response, "beforeend")
        retarget(response, "#modal-wrapper")

        return trigger_client_event(response, "show-modal", after="swap")


def _check_progress(request, code, number):
    slug = code + "-" + str(number)
    progress = QuizProgress.objects.filter(
        session=request.session.session_key, quiz=slug
    )
    if progress.exists():
        context = {"quiz": Quiz.objects.get(slug=slug)}
        response = TemplateResponse(request, "quiz/confirmation.html", context)
        return response
    else:
        return None


@htmx_required
def _check_answer(request):
    slug = request.headers["code"] + "-" + str(request.headers["number"])
    progress = get_object_or_404(
        QuizProgress, session=request.session.session_key, quiz=slug
    )
    index = progress.index
    qid = progress.key[str(index)]
    question = BaseQuestion.objects.get(pk=qid["question"])
    question.attempts += 1
    if (qtype := question.get_type()) == "multiplechoicequestion":
        MultipleChoiceAnswer.objects.filter(id=qid["user_choice"]).update(picked=F("picked") + 1)
    elif qtype == "truefalsequestion":
        TrueFalseQuestion.objects.filter(id=qid["question"]).update(accuracy=F("accuracy") + 1)
    # Needs logic to highlight the selected answer in green client side
    if str(request.POST.get("answer")) == str(qid["correct"]):
        _save_progress(request)
        response = _next_question(request)
        return response
    else:
        q_obj = BaseQuestion.objects.select_related().get(id=qid["question"])
        hint = q_obj.hint
        context = {"hint": hint}
        response = TemplateResponse(request, "quiz/hint.html", context)
        reswap(response, "beforeend")
        retarget(response, "#modal-wrapper")
        return trigger_client_event(response, "show-modal", after="swap")


@htmx_required
def _grade_quiz(request):
    slug = request.headers["code"] + "-" + str(request.headers["number"])
    progress = get_object_or_404(
        QuizProgress, session=request.session.session_key, quiz=slug
    )
    quiz = progress.key
    total_q = 0
    total_q = progress.index
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
        "code": request.headers["code"],
        "number": request.headers["number"],
    }
    if request.user.is_authenticated:
        Result.objects.create(
            user=request.user,
            quiz=slug,
            # elapsed=<To be replaced with time it took to complete quiz
            total=total_q,
            correct=n_correct,
            key=quiz,
        )
    response = TemplateResponse(request, "quiz/completed.html", context)
    return retarget(response, "#page-wrapper")
