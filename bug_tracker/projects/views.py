from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required  # auth
from .decorators import allowed_users


# Create your views here.
@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["admin", "developer", "tester", "manager"])
def index(request):
    return render(request, "projects/home.html", {})


@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["admin", "manager"])
def create(request):
    return render(request, "projects/form.html", {})


@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["admin", "manager"])
def update(request, id):
    return render(request, "projects/form.html", {})


@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["admin", "manager"])
def delete(request, id):
    return redirect(index)


@login_required(login_url="/users/login")
def restricted(request):
    return render(request, "projects/restricted.html", {})
