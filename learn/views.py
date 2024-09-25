from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .models import Course, Lesson
from pages.models import Pages


@login_required
def course_index(request) -> HttpResponse:
    # page = Pages.objects.get("Courses")
    courses = Course.objects.all().order_by("name")
    return render(
        request,
        "course_list.html",
        {
            # "page": page,
            "courses": courses,
        },
    )


@login_required
def course_landing_page(request, code) -> HttpResponse:
    page = Pages.objects.get(f"{code} Lesson Intro")
    course = get_object_or_404(Course, pk=code)
    return render(
        request,
        "unit_landing_page.html",
        {
            "learn_topic": course,
            "page": page,
        },
    )


def return_task_list(request, code) -> HttpResponse:
    # page = Pages.objects.get(f"{code} Task List")
    course = get_object_or_404(Course, pk=code)
    task_list = course.get_task_list()
    return render(
        "Replace with template",
        {
            "task_list": task_list,
            # "page": page
        },
    )


def lesson_page(request, code, page) -> HttpResponse:
    lesson = Lesson.objects.filter(code=code, page=page).order_by("page")
    return render("Replace with template", {"lesson": lesson})
