from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.template.response import TemplateResponse
from django.views.generic import ListView

from abarocks.utils import for_htmx
from .models import Course, Lesson, Task
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
        "learn/unit_landing_page.html",  # TODO: Check tempalte name
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


@for_htmx(use_block="options")
def task_changeform_options(request):
    course_filter = Task.objects.filter(license=request.GET.get("license"))
    if course_filter.exists():
        categories = course_filter.values("area", "area_name").distinct()
        options = {}
        for entry in categories:
            options[entry["area"]] = entry["area_name"]
        return TemplateResponse(request, "learn/change_form.html", {"options": options})
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
