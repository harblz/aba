from allauth.account import forms as allauth
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import SupportTicket


class SignupForm(allauth.SignupForm):

    def save(self, request):
        user = super().save(request)
        return user


class LoginForm(allauth.LoginForm):

    def login(self, *args, **kwargs):
        return super().login(*args, **kwargs)


class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name")


class SupportTicketForm(ModelForm):
    class Meta:
        model = SupportTicket
        fields = ("type", "message")
