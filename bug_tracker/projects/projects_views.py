from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .decorators import allowed_users
from .models import Project, User
from .forms import ProjectForm, ManageAccessForm


# CRUD
@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["admin", "developer", "tester", "manager"])
def read_projects(request):
    projects = request.user.project_set.all()
    return render(
        request,
        "projects/projects.html",
        {"projects": projects}
    )


@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["manager"])
def create_project(request):
    if request.POST:
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            project.team.add(request.user)
            project.save()
            return redirect("/")
    else:
        form = ProjectForm()

    return render(
        request,
        "projects/project_form.html",
        {"form": form}
    )


@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["manager"])
def update_project(request, project_id):
    project = Project.objects.get(id=project_id)

    if request.POST:
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = ProjectForm(instance=project)

    return render(
        request,
        "projects/project_form.html",
        {"form": form}
    )


@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["manager"])
def delete_project(request, project_id):
    Project.objects.filter(id=project_id).delete()
    return redirect("/")


# ACCESS
@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["manager"])
def allow_access(request, project_id):
    form = ManageAccessForm()
    project = Project.objects.get(id=project_id)

    if request.POST:
        project.team.add(request.POST["member"])
        project.save()

    return render(
        request,
        "projects/access.html",
        {"form": form, "project": project}
    )


@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["manager"])
def deny_access(request, project_id, user_id):
    project = Project.objects.get(id=project_id)
    user = User.objects.get(id=user_id)

    project.team.remove(user)
    project.save()

    return redirect("/allow_access/" + str(project_id))