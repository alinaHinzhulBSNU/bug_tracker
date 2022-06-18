from django.contrib.auth import login, logout
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect

from .forms import RegisterForm, LoginForm
from .decorators import unauthenticated_user


@unauthenticated_user
def register(request):
    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name=request.POST["role"])
            user.groups.add(group)
            login(request, user)
            return redirect("/")
    else:
        form = RegisterForm()

    return render(
        request,
        "users/register.html",
        {
            "form": form
        }
    )


@unauthenticated_user
def sign_in(request):
    form = LoginForm(request.POST or None)

    if request.POST and form.is_valid():
        user = form.login(request)
        if user:
            login(request, user)
            return redirect("/")

    return render(
        request,
        "registration/login.html",
        {
            "form": form
        }
    )


def log_out(request):
    logout(request)
    return redirect("/users/login")
