from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseServerError, HttpResponseForbidden
from django.views.generic import ListView
import random
from django_htmx.http import retarget, trigger_client_event

from learn.models import Profile, Course
from pages.models import Pages
from .models import *
from .forms import QuizForm


class QuizIndex(ListView):
    model = Quiz

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page"] = Pages.objects.get(title="Practice Quizzes")
        return context


class IndexByCourse(ListView):
    model = Quiz

    def get_queryset(self):
        queryset = Quiz.objects.filter(self.kwargs["course"])
        return queryset


def get_quiz(request, course, quiz) -> HttpResponse:
    return render(
        request,
        "",  # TODO: Replace with template name
        {"course": course, "quiz": quiz},
    )


def _get_questions(code, quiz) -> list:
    weights = Course.objects.get(code=code).weights
    questions = []
    for key, value in weights:
        options = Question.objects.filter(
            code=code, quiz=quiz, category=key
        ).values_list("id")
        questions += random.sample(options, value)
    return questions


def _save_progress(request) -> None:
    # TODO: Add session saving
    pass
    # response =
    # return trigger_client_event(response)


def _next_question(request, question) -> HttpResponse:
    if request.htmx:
        try:
            _save_progress(request)
        except Exception as e:
            return HttpResponseServerError(e)

        try:
            question = Question.objects.get(id=question)
            form = QuizForm(question=question)
            return retarget(
                request,
                "",  # TODO: Replace with template name
            )
        except Exception as e:
            return HttpResponseServerError(e)
    else:
        return HttpResponseForbidden()


def _start_quiz(request, code, quiz) -> HttpResponse:
    if request.htmx:
        try:
            questions = _get_questions(code, quiz)
            random.shuffle(questions)
            if quiz.values("timed"):
                time = quiz.values_list("time")
                # Save start time to session
            form = QuizForm(question=Question.objects.get(pk=questions[0]))
            response = render(
                request,
                "",  # TODO: Replace with template name
                {"form": form, "question_list": questions},
            )
            return retarget(
                response,
                "",  # TODO: Replace with CSS selector
            )
        except Exception as e:
            return HttpResponse("There was a problem with your request:" + str(e))
    else:
        return HttpResponseForbidden()


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
