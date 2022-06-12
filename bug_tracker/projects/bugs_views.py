from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .decorators import allowed_users
from .models import Project


@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["admin", "developer", "tester", "manager"])
def read_bugs(request, id):
    project = Project.objects.get(id=id)
    return render(
        request,
        "projects/bugs.html",
        {"project": project})