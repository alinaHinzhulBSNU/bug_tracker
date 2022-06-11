import datetime

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import csv
from .decorators import allowed_users
from .forms import ProjectForm, TaskForm, ManageAccessForm
from .models import Project, Task
from .helpers import get_status_by_value


# PROJECTS
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


@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["admin", "developer", "tester", "manager"])
def dashboard(request, project_id):
    project = Project.objects.get(id=project_id)

    to_do = project.task_set.filter(status=get_status_by_value("to do"))
    doing = project.task_set.filter(status=get_status_by_value("doing"))
    done = project.task_set.filter(status=get_status_by_value("done"))

    return render(
        request,
        "projects/dashboard.html",
        {
            "project_id": project_id,
            "to_do": to_do,
            "doing": doing,
            "done": done,
        }
    )


# TASKS
@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["admin", "developer", "tester", "manager"])
def read_tasks(request, project_id):
    project = Project.objects.get(id=project_id)

    return render(
        request,
        "projects/tasks.html",
        {"project": project}
    )


@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["admin", "developer", "tester", "manager"])
def read_task(request, project_id, task_id):
    task = Task.objects.get(id=task_id)

    return render(
        request,
        "projects/task.html",
        {"prediction": "",
         "task": task,
         "project_id": project_id})


@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["manager"])
def add_task(request, project_id):
    project = Project.objects.get(id=project_id)
    form = TaskForm(project=project, initial={"project": project})

    if request.POST:
        task = form.save(commit=False)

        task.text = request.POST["text"]
        task.severity = request.POST["severity"]
        task.status = request.POST["status"]
        task.performer = User.objects.get(id=request.POST["performer"])
        task.project = project

        task.save()

        return redirect("/tasks/" + str(project_id))

    return render(
        request,
        "projects/task_form.html",
        {"form": form, "project": project}
    )


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

    return render(
        request,
        "projects/task_form.html",
        {"form": form}
    )


@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["manager"])
def delete_task(request, project_id, task_id):
    Task.objects.filter(id=task_id).delete()
    return redirect("/tasks/" + str(project_id))


@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["admin", "developer", "tester", "manager"])
def add_task_to_dashboard(request, project_id, task_id):
    task = Task.objects.get(id=task_id)
    task.status = get_status_by_value("to do")
    task.start_time = datetime.datetime.now()
    task.save()

    return redirect("/tasks/" + str(project_id))


@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["admin", "developer", "tester", "manager"])
def delete_task_from_dashboard(request, project_id, task_id):
    task = Task.objects.get(id=task_id)
    task.status = get_status_by_value("backlog")
    task.start_time = None
    task.save()

    return redirect("/tasks/" + str(project_id))


@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["admin", "developer", "tester", "manager"])
def load_tasks_in_csv(request, project_id):
    project = Project.objects.get(id=project_id)

    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="tasks.csv"'},
    )

    writer = csv.writer(response)
    for task in project.task_set.all():
        writer.writerow([task.id,
                         task.text,
                         task.get_severity(),
                         task.get_status(),
                         task.performer.username])

    return response


@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["admin", "developer", "tester", "manager"])
def set_task_to_do(request, project_id, task_id):
    task = Task.objects.get(id=task_id)

    task.status = get_status_by_value("to do")
    task.start_time = datetime.datetime.now()
    task.end_time = None

    task.save()

    return redirect("/dashboard/" + str(project_id))


@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["admin", "developer", "tester", "manager"])
def set_task_doing(request, project_id, task_id):
    task = Task.objects.get(id=task_id)

    task.status = get_status_by_value("doing")
    task.end_time = None

    task.save()

    return redirect("/dashboard/" + str(project_id))


@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["admin", "developer", "tester", "manager"])
def set_task_done(request, project_id, task_id):
    task = Task.objects.get(id=task_id)

    task.status = get_status_by_value("done")
    task.end_time = datetime.datetime.now()

    task.save()

    return redirect("/dashboard/" + str(project_id))


# Predict time for task
@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["admin", "developer", "tester", "manager"])
def predict_for_task(request, project_id, task_id):
    prediction = "No prediction"
    task = Task.objects.get(id=task_id)

    return render(request,
                  "projects/task.html",
                  {"prediction": prediction,
                   "task": task,
                   "project_id": project_id})


# BUGS
@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["admin", "developer", "tester", "manager"])
def read_bugs(request, id):
    project = Project.objects.get(id=id)
    return render(
        request,
        "projects/bugs.html",
        {"project": project})


# STATISTIC
@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["admin", "developer", "tester", "manager"])
def get_statistic(request, id):
    project = Project.objects.get(id=id)
    return render(request, "projects/statistic.html", {"project": project})


# RESTRICTED
@login_required(login_url="/users/login")
def restricted(request):
    return render(request, "projects/restricted.html", {})



