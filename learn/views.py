from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import ListView

from .models import Course, Lesson
from pages.models import Pages


class CourseIndex(ListView):
    model = Course

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
        "unit_landing_page.html",  # TODO: Check tempalte name
        {
            "learn_topic": course,
            # "page": page,
        },
    )


class TaskListView(ListView):
    model = Course

    def get_queryset(self):
        queryset = get_object_or_404(Course, code=self.kwargs["code"])
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task_list"] = Course.objects.get(
            code=self.kwargs["code"]
        ).get_task_list()
        return context


def lesson_page(request, course) -> HttpResponse:
    page = int(request.GET.get("page", "1"))
    lesson = Lesson.objects.get(course=course, page=page)
    return render(
        request,
        "",  # TODO: Replace with template name
        {"lesson": lesson, "page": page},
    )
