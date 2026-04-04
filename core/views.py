from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView
from django.conf import settings
from django.dispatch import receiver

from allauth.account.signals import email_confirmed

from core.forms import SignupForm
from core.models import User, Profile
from quiz.models import Result as QResult
from safmeds.models import Result as SResult
from .forms import SupportMessageForm, UserUpdateForm


@receiver(email_confirmed)
def email_confirmed_(request, email_address, **kwargs):
    user = email_address.user
    user.email_verified = True

    user.save()


@login_required
def user_profile(request):
    profile = Profile.objects.select_related("user").get(user=request.user.id)
    name = ""
    if request.user.first_name:
        name = request.user.first_name
    else:
        name = request.user.username
    data = profile.data
    quiz_results = QResult.objects.filter(user=request.user.id)
    safmeds_results = SResult.objects.filter(user=request.user.id)
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


def edit_profile(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("/account")

    else:
        form = UserUpdateForm(instance=request.user)
        context = {"form": form}
        return render(request, "update_profile.html", context)


class ContactUs(FormView):
    form_class = SupportMessageForm
