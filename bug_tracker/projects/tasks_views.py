import datetime
import csv

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .decorators import allowed_users
from .forms import TaskForm
from .models import Project, Task
from .helpers import get_status_by_value
from .analytics import predict_time_for_task_by_ml


# CRUD
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
        task.severity = int(request.POST["severity"])
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
        task.severity = int(request.POST["severity"])
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


# DISPLAY OR HIDE ON DASHBOARD
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


# CHANGE STATUS
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


# CSV LOADING
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


# ML PREDICTION
@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["admin", "developer", "tester", "manager"])
def predict_for_task(request, project_id, task_id):
    task = Task.objects.get(id=task_id)

    project = Project.objects.get(id=project_id)
    tasks = project.task_set.filter(status=get_status_by_value("done"))

    prediction = predict_time_for_task_by_ml(task.performer, task.severity, tasks)

    return render(request,
                  "projects/task.html",
                  {"prediction": prediction,
                   "task": task,
                   "project_id": project_id})