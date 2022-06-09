from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .decorators import allowed_users
from .forms import ProjectForm, TaskForm, ManageAccessForm
from .models import Project, Task
from .helpers import get_status_by_value


# PROJECTS
# Read projects
@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["admin", "developer", "tester", "manager"])
def index(request):
    projects = request.user.project_set.all()
    return render(request, "projects/projects.html", {"projects": projects})


# Create project
@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["manager"])
def create(request):
    if request.POST:
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            project.team.add(request.user)
            project.save()
            return redirect(index)
    else:
        form = ProjectForm()

    return render(request, "projects/project_form.html", {"form": form})


# Update project
@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["manager"])
def update(request, id):
    project = Project.objects.get(id=id)

    if request.POST:
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect(index)
    else:
        form = ProjectForm(instance=project)

    return render(request, "projects/project_form.html", {"form": form})


# Delete project
@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["manager"])
def delete(request, id):
    Project.objects.filter(id=id).delete()
    return redirect(index)


# Allow access to project
@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["manager"])
def allow_access(request, id):
    form = ManageAccessForm()
    project = Project.objects.get(id=id)

    if request.POST:
        project.team.add(request.POST["member"])
        project.save()

    return render(request, "projects/access.html", {"form": form, "project": project})


# Deny access to project
@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["manager"])
def deny_access(request, project_id, user_id):
    project = Project.objects.get(id=project_id)
    user = User.objects.get(id=user_id)

    project.team.remove(user)
    project.save()

    return redirect("/allow_access/" + str(project_id))


# Display project
@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["admin", "developer", "tester", "manager"])
def dashboard(request, id):
    project = Project.objects.get(id=id)
    return render(request, "projects/dashboard.html", {"project": project})


# TASKS
# Read tasks
@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["admin", "developer", "tester", "manager"])
def tasks(request, id):
    project = Project.objects.get(id=id)
    return render(request, "projects/tasks.html", {"project": project})


# Add task
@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["manager"])
def add_task(request, id):
    project = Project.objects.get(id=id)
    form = TaskForm(project=project, initial={"project": project})

    if request.POST:
        task = form.save(commit=False)

        task.text = request.POST["text"]
        task.severity = request.POST["severity"]
        task.status = request.POST["status"]
        task.performer = User.objects.get(id=request.POST["performer"])
        task.project = project

        task.save()

        return redirect("/tasks/" + str(id))

    return render(request, "projects/task_form.html", {"form": form, "project": project})


# Update task
@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["manager"])
def update_task(request, project_id, task_id):
    project = Project.objects.get(id=project_id)
    task = Task.objects.get(id=task_id)

    if request.POST:
        task.text = request.POST["text"]
        task.severity = request.POST["severity"]
        task.status = request.POST["status"]
        task.performer = User.objects.get(id=request.POST["performer"])
        task.save()
        return redirect("/tasks/" + str(project_id))
    else:
        form = TaskForm(project=project, instance=task)

    return render(request, "projects/task_form.html", {"form": form})


# Delete task
@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["manager"])
def delete_task(request, project_id, task_id):
    Task.objects.filter(id=task_id).delete()
    return redirect("/tasks/" + str(project_id))


# Add task to dashboard
@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["admin", "developer", "tester", "manager"])
def add_to_dashboard(request, project_id, task_id):
    task = Task.objects.filter(id=task_id)
    task.status = "1"  # to do
    task.save()
    return redirect("/tasks/" + str(project_id))


# Add task to dashboard
@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["admin", "developer", "tester", "manager"])
def add_to_dashboard(request, project_id, task_id):
    task = Task.objects.get(id=task_id)
    task.status = get_status_by_value("to do")
    task.save()
    return redirect("/tasks/" + str(project_id))


# Remove task from dashboard
@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["admin", "developer", "tester", "manager"])
def delete_from_dashboard(request, project_id, task_id):
    task = Task.objects.get(id=task_id)
    task.status = get_status_by_value("backlog")
    task.save()
    return redirect("/tasks/" + str(project_id))


# RESTRICTED
@login_required(login_url="/users/login")
def restricted(request):
    return render(request, "projects/restricted.html", {})



