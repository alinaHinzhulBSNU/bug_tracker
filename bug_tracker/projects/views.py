from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .decorators import allowed_users
from .forms import CreateProject, ManageAccessForm
from .models import Project


# Create your views here.
@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["developer", "tester", "manager"])
def index(request):
    projects = request.user.project_set.all()
    return render(request, "projects/home.html", {"projects": projects})


@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["manager"])
def create(request):
    if request.POST:
        form = CreateProject(request.POST)
        if form.is_valid():
            project = form.save()
            project.team.add(request.user)
            project.save()
            return redirect(index)
    else:
        form = CreateProject()

    return render(request, "projects/form.html", {"form": form})


@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["manager"])
def update(request, id):
    project = Project.objects.get(id=id)

    if request.POST:
        form = CreateProject(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect(index)
    else:
        form = CreateProject(instance=project)

    return render(request, "projects/form.html", {"form": form})


@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["manager"])
def delete(request, id):
    Project.objects.delete(id)
    return redirect(index)


@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["manager"])
def manage_access(request, id):
    form = ManageAccessForm()
    project = Project.objects.get(id=id)

    if request.POST:
        project.team.add(request.POST["member"])
        project.save()

    return render(request, "projects/access.html", {"form": form, "project": project})


@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["manager"])
def deny_access(request, project_id, user_id):
    project = Project.objects.get(id=project_id)
    user = User.objects.get(id=user_id)

    project.team.remove(user)
    project.save()

    return redirect("/access/" + str(project_id))


@login_required(login_url="/users/login")
def restricted(request):
    return render(request, "projects/restricted.html", {})
