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

from .models import Course, Unit

# Create your views here.
def course_index(request):
    pages           = Pages.objects.order_by('order')
    units 			= Unit.objects.order_by('unit_order')
    return render(request, 'course_list.html', { 'pages': pages, 'units': units })

# Create your views here.
def course_account(request):
    pages           = Pages.objects.order_by('order')
    return render(request, 'account.html', { 'pages': pages })