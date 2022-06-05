from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from .decorators import unauthenticated_user


@unauthenticated_user
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name=request.POST["role"])
            user.groups.add(group)
            login(request, user)
            return redirect("/")
    else:
        form = RegisterForm()

    return render(request, "users/register.html", {"form": form})


@unauthenticated_user
def sign_in(request):
    form = AuthenticationForm()

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/")

    return render(request, "registration/login.html", {"form": form})


def log_out(request):
    logout(request)
    return redirect("/users/login")

