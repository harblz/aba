from typing import Type
from traceback import format_exc

from django.shortcuts import get_object_or_404, render, Http404
from django.http import HttpResponse, HttpResponseServerError, HttpResponseForbidden
from django.views.generic import ListView
import random
from django_htmx.http import retarget, trigger_client_event, reswap
from django.utils import timezone
from django.template.response import TemplateResponse
from django.apps import apps

from pages.models import Pages
from learn.models import Course, Lesson, Task, ContentArea
from core.models import Profile
from .models import *
from .forms import TakeQuizForm
from core.decorators import htmx_required
from abarocks.views import handler500


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
def _save_progress(request):
    slug = request.GET.get("slug")
    index = request.session["quiz"][slug]["current_index"]
    request.session["quiz"][slug]["questions"][str(index)]["user_answer"] = (
        request.POST.get("answer")
    )
    index += 1

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


@htmx_required
def _next_question(request) -> HttpResponse:
    _save_progress(request)
    slug = request.POST.get("slug")
    next_index = request.session["quiz"][slug]["current_index"]
    model = apps.get_model("quiz", next_index["table"])
    question = model.objects.get(pk=next_index["question"])
    form = TakeQuizForm(question=question)
    if next_index["table"] == "MultipleChoiceQuestion":
        form.fields["answer"].choices = [
            (answer.id, answer.text) for answer in question.answers.all()
        ]
    elif next_index["table"] == "TrueFalseQuestion":
        form.fields["answer"].choices = [(True, "True"), (False, "False")]
    return render(request, "quiz/question_form.html", {"form": form})


@htmx_required
def _start_quiz(request, code, number) -> HttpResponse:
    quiz = Quiz.objects.get(course=code, number=number)
    request.session["quiz"] = {}
    request.session["quiz"][quiz.slug] = {}
    request.session["quiz"][quiz.slug]["current_index"] = 0
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
    model = apps.get_model("quiz", first_question["table"])
    question = model.objects.get(pk=first_question["question"])
    choices = []
    if first_question["table"] == "MultipleChoiceQuestion":
        choices = [(answer.id, answer.text) for answer in question.answers.all()]
    elif first_question["table"] == "TrueFalseQuestion":
        choices = [(True, "True"), (False, "False")]
    form = TakeQuizForm()
    form.fields["answer"].choices = choices

    response = TemplateResponse(
        request,
        "quiz/question_form.html",
        {"form": form, "slug": quiz.slug, "question": question},
    )
    return response


"""def submit_score_report(request):
    # send_mail('Subject here','Here is the message.','alex@behaviorist.tech',['alex@behaviorist.tech'],fail_silently=False,)
    score = request.POST.get("quiz_score")

    unit_id = request.POST.get("unit_id")
    unit = Unit.objects.get(pk=unit_id)

    form_id = request.POST.get("form_id")
    form = Form.objects.get(pk=form_id)

    if score >= "0.8":
        profile = Profile.course_lessons_completed.all
        profile.add(request.POST.get("form_id"))
        profile.save()

    results = QuizScore(score=score, unit_id=unit, form_id=form, date=datetime.now())
    results.save()

    return JsonResponse(
        {
            "unit_id": unit_id,
            "form_id": form_id,
            "score": score,
        }
    )


def quiz_missed_questions_report(request):
    request.POST.get("questions")
    report = []

    for question in questions:
        missed_question = Question.objects.filter(pk=question[0]).values_list()
        task_list_item = Task.objects.filter(
            pk=missed_question.task_list_item_id
        ).values_list()
        report.append(
            [
                missed_question,
                task_list_item,
            ]
        )

    return JsonResponse(
        {
            "report": report,
        }
    )


def quiz_view(request, quiz_id, form_id):
    pages = Pages.objects.order_by("order")
    # get
    if request.method == "GET":
        quiz_name = Unit.objects.get(pk=quiz_id)
        queryset_ids = Question.objects.filter(
            unit_id=quiz_id, form_id=form_id
        ).values_list("id", flat=True)
        unit_name = quiz_name
        unit_id = quiz_id
        max_questions = len(queryset_ids)

        return render(
            request,
            "quiz/quiz.html",
            {
                "form_id": form_id,
                "question_ids": json.dumps(list(queryset_ids), cls=DjangoJSONEncoder),
                "unit_name": unit_name,
                "unit_id": unit_id,
                "total_questions": max_questions,
                "pages": pages,
            },
        )

    # post
    else:
        form_name = Form.objects.get(pk=form_id).form_name
        form_short_name = Form.objects.get(pk=form_id).form_short_name
        next_question_id = request.POST.get("next_question_id")
        prev_question_id = request.POST.get("prev_question_id")
        quiz_id = request.POST.get("unit_id")

        quiz_name = Unit.objects.get(id=quiz_id)

        task_list_ids = (
            Question.objects.filter(unit_id=quiz_id, form_id=form_id)
            .values_list("task_list_item_id", flat=True)
            .distinct()
        )
        task_list = Task.objects.filter(pk__in=task_list_ids).values_list()

        # 1 at the end of the test, don't worry if there is no next question
        try:
            next_question = Question.objects.get(pk=next_question_id)

        except (KeyError, Question.DoesNotExist):
            next_question = None

        if next_question == None:
            next_question_choices = None
            next_question_question_text = None
            next_question_question_hint = None
        else:
            next_question = Question.objects.get(pk=next_question_id)
            next_question_choices = Choice.objects.filter(question_id=next_question_id)
            next_question_choices = [
                {"id": item.id, "choice": item.choice_text}
                for item in next_question_choices
            ]
            next_question = list(
                Question.objects.filter(pk=next_question_id).values_list(
                    "id", "question_text", "question_hint", "task_list_item_id"
                )
            )

        # 2 at the start of the test, don't worry if there is no prev question
        try:
            prev_question = Question.objects.get(pk=prev_question_id)

        except (KeyError, Question.DoesNotExist):
            prev_question = None

        if prev_question == None:
            choices = list(
                Choice.objects.filter(question_id=next_question_id)
                .order_by("?")
                .values_list("id", "choice_text", "is_correct")
            )
            prev_question = None
            prev_correct_choice = None
            prev_question_hint = None

        else:
            choices = list(
                Choice.objects.filter(question_id=next_question_id)
                .order_by("?")
                .values_list("id", "choice_text", "is_correct")
            )
            prev_question = list(
                Question.objects.filter(pk=prev_question_id).values_list(
                    "id", "question_text", "question_hint", "task_list_item_id"
                )
            )
            prev_correct_choice = list(
                Choice.objects.filter(
                    question_id=prev_question_id, is_correct=True
                ).values_list("choice_text")
            )
            prev_question_hint = prev_question[0][2]

        task_item = Task.objects.get(pk=next_question[0][3]).task_name

        return JsonResponse(
            {
                "form": form_name,
                "form_id": form_id,
                "form_short_name": form_short_name,
                #'task_item'             : serializers.serialize('json', list(task_item), ensure_ascii=False),
                #'task_list'             : serializers.serialize('json', task_list),
                "unit_name": quiz_name.unit_name,
                "choices": choices,
                "next_question": next_question,
                "prev_question": prev_question,
                "prev_question_hint": prev_question_hint,
                "prev_correct_choice": prev_correct_choice,
                "task_item": task_item,
            }
        )"""
