from django.shortcuts import get_object_or_404, render, Http404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.template.response import TemplateResponse
from django.views.generic import ListView

from .models import Course, Lesson, Task, ContentArea
from quiz.models import Quiz
from core.decorators import htmx_required


def lessons(request, code):
    try:
        course = get_object_or_404(Course, code=code)
        course_lessons = Lesson.objects.filter(course_id=code).order_by("course__name")
    except Lesson.DoesNotExist:
        raise Http404("This lesson does not exist.")
    return render(
        request,
        "learn/lessons_landing_page.html",
        {"course": course, "lessons": lessons},
    )


def quiz_lessons(request, quiz_slug):
    lessons = ""
    try:
        quizzes = Quiz.objects.filter(slug=quiz_slug).prefetch_related("areas")
        for quiz in quizzes:
            for area in quiz.areas.all():
                lessons += Lesson.objects.filter(area=area).order_by("course__name")
    except Quiz.DoesNotExist:
        raise Http404("This quiz does not exist.")
    return render(request, "learn/quiz_lesson_page.html", {"lessons": lessons})


def Courses(request, code):
    course = get_object_or_404(Course, code=code)
    quizzes = (
        Quiz.objects.filter(course_id=code)
        .order_by("course__name")
        .prefetch_related("areas")
    )
    return render(
        request,
        "learn/course_landing_page.html",
        {"course": course, "quizzes": quizzes},
    )


class CourseIndex(ListView):
    model = Course
    context_object_name = "Courses"
    template_name = "learn/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["page"] = Pages.objects.get("Courses")
        return context


@login_required
def course_landing_page(request, code) -> HttpResponse:
    # page = Pages.objects.get(f"{code} Lesson Intro")
    course = get_object_or_404(Course, pk=code)
    return render(
        request,
        "learn/course_landing_page.html",  # TODO: Check template name
        {
            "learn_topic": course,
            # "page": page,
        },
    )


class TaskListView(ListView):
    model = Course
    template_name = "learn/task_list.html"

    def get_queryset(self):
        queryset = get_object_or_404(Course, code=self.kwargs["code"])
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task_list"] = Course.objects.get(
            code=self.kwargs["code"]
        ).get_task_list()
        context["license"] = self.kwargs["code"]
        return context


def lesson_page(request, course) -> HttpResponse:
    page = request.GET.get("page")
    lesson = Lesson.objects.get(course=course, page=page)
    # TODO: Determine logic for saving sessions and handling users
    return render(
        request,
        "learn/course_landing_page.html",
        {"lesson": lesson, "page": page},
    )


def _next_page(request, course) -> HttpResponse:
    # Pull current page from session/profile
    # Increment page # and query for ID
    pass


@htmx_required
def task_changeform_options(request):
    if request.GET.get("license") == "BCaBA":
        course_filter = ContentArea.objects.filter(license="BCBA")
    else:
        course_filter = ContentArea.objects.filter(license=request.GET.get("license"))
    if course_filter.exists():
        areas = {}
        for index, slug in enumerate(course_filter.values_list("slug", flat=True)):
            areas[slug] = str(course_filter[index])
        return TemplateResponse(
            request,
            "learn/partial/_options.html",
            {"areas": areas},
        )
    else:
        pass


def get_area_name(request):
    if request.htmx:
        area = (
            Task.objects.filter(area=request.GET.get("area"))
            .values_list("area_name", flat=True)
            .distinct()
        )
        return area
