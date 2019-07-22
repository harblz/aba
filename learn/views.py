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

from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.db.models import F
import random

from django.utils import timezone
from datetime import datetime    

from pages.models import Pages

from .models import Course, Unit, LessonPage

def course_index(request):
    pages           = Pages.objects.order_by('order')
    units 			= Unit.objects.order_by('unit_order')
    lesson_page		= LessonPage.objects.order_by('unit_order')
    return render(request, 'course_list.html', { 'pages': pages, 'units': units })

def unit_landing_page(request, pk):
	pages 			= Pages.objects.order_by('order')
	return render(request, 'unit_landing_page.html', { 'pages':pages })

def course_account(request):
    pages           = Pages.objects.order_by('order')
    return render(request, 'account.html', { 'pages': pages })

# Pages written via the learn dashboard
def topic_page(request, slug):
	pages = Pages.objects.order_by('order')
	page = LessonPage.objects.filter(slug=slug)
	page = get_object_or_404(LessonPage, pk=page[0].id)
	page.page_views += 1;
	page.save()
	return render(request, 'learn_topic.html', {'learn_topic': learn_topic, 'pages': pages})