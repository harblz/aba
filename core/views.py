from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView
from django.conf import settings

from core.forms import SignupForm
from core.models import User, Profile
from quiz.models import Result as qresult
from safmeds.models import Result as sresult
from .forms import SupportMessageForm


@login_required
def user_profile(request):
    profile = Profile.objects.select_related("user").get(user=request.user.id)
    name = ""
    if request.user.first_name:
        name = request.user.first_name
    else:
        name = request.user.username
    data = profile.data
    quiz_results = qresult.objects.filter(user=request.user.id)
    safmeds_results = sresult.objects.filter(user=request.user.id)
    title = f"Welcome back, {name}!"
    subtitle = ""
    blurb = ""
    context = {
        "title": title,
        "subtitle": subtitle,
        "blurb": blurb,
        "data": data,
        "quizzes": quiz_results,
        "safmeds_attempts": safmeds_results,
    }
    return render(request, "profile.html", context)


class ContactUs(FormView):
    form_class = SupportMessageForm
