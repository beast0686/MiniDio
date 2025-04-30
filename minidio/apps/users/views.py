from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import UserAuthenticationForm, UserRegistrationForm


class UserLoginView(LoginView):
    form_class = UserAuthenticationForm
    template_name = "login.html"

    def get_success_url(self) -> str:
        return reverse_lazy("landing")


class UserRegisterView(CreateView):
    form_class = UserRegistrationForm
    template_name = "login.html"
    success_url = reverse_lazy("login")


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    messages.success(request, "You have been logged out.", "is-info")
    return redirect(reverse_lazy("homepage"))
