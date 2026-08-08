from allauth.account.signals import email_confirmed
from django.contrib.auth.decorators import login_required
from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.views.generic import FormView

from core.models import Profile, SupportTicket
from quiz.models import Result as QResult
from safmeds.models import Result as SResult
from .forms import SupportTicketForm, UserUpdateForm


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
    tickets = SupportTicket.objects.filter(user=request.user.id)
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
        "tickets": tickets,
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
    form_class = SupportTicketForm
    template_name = "contact_us.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def support_ticket(request, id):
    ticket = SupportTicket.objects.select_related().get(pk=id)
