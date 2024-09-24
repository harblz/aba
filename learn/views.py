from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from .models import Course, Lesson


@login_required
def course_index(request):
    courses = Course.objects.all().order_by("name")
    return render(
        request,
        "course_list.html",
        {
            # "pages": pages,
            "courses": courses,
        },
    )


@login_required
def course_landing_page(request, code):
    course = get_object_or_404(Course, pk=code)
    return render(
        request,
        "unit_landing_page.html",
        {
            "learn_topic": course,
            # "pages": pages,
        },
    )


def return_task_list(request, code):
    course = get_object_or_404(Course, pk=code)
    task_list = course.get_task_list()
    return render("Replace with template", {"task_list": task_list})


def lesson_page(request, code, page):
    lesson = Lesson.objects.get(code=code, page=page)
    return render("Replace with template", {"lesson": lesson})
