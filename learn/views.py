from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.views.generic import TemplateView

import json

from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict

from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.db.models import F
import random

from django.utils import timezone
from datetime import datetime


from .models import Course, Profile


@login_required
def course_index(request):
    units = Unit.objects.order_by("unit_order")
    lesson_page = LessonPage.objects.order_by("unit_order")

    # chart progress and labels list for chart.js
    # chart_progress_array 	= Profile.objects.values_list('course_units_completed', flat=True)
    chart_progress_array = Profile.objects.values("id", "course_units_completed").all()

    # all_units = Unit.objects.order_by('unit_order').values_list('unit_weight', flat=True)
    for unit in chart_progress_array:
        unit["course_weight"] = 10

    chart_progress_array = list(chart_progress_array)

    chart_labels_array = Unit.objects.values_list("unit_name", flat=True)
    chart_labels_array = list(chart_labels_array)

    return render(
        request,
        "course_list.html",
        {
            # 'pages'					: pages,
            "units": units,
            "lesson_page": lesson_page,
            "chart_labels_array": chart_labels_array,
            "chart_progress_array": chart_progress_array,
        },
    )


@login_required
def unit_landing_page(request, pk):
    page = LessonPage.objects.filter(pk=pk)
    page = get_object_or_404(LessonPage, pk=page[0].id)
    page.page_views += 1
    page.save()
    return render(
        request,
        "unit_landing_page.html",
        {
            "learn_topic": page,
            "pages": pages,
        },
    )


@login_required
def course_account(request):
    return render(request, "account.html", {"pages": pages})


# Pages written via the learn dashboard
@login_required
def topic_page(request, slug):
    page = LessonPage.objects.filter(slug=slug)
    page = get_object_or_404(LessonPage, pk=page[0].id)
    page.page_views += 1
    page.save()
    return render(request, "learn_topic.html", {"learn_topic": page, "pages": pages})
