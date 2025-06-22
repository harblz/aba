from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.conf import settings

from core.forms import SignupForm
from core.models import User


class SignUpView(CreateView):
    form_class = SignupForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


@login_required
def user_profile(request):
    user = User.objects.get(username=request.user.username)
    return render(request, "profile.html", {"user": user})
