from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Project
from .decorators import allowed_users
from .helpers import get_status_by_value
from .analytics import get_data_for_statistics


# DASHBOARD
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


# STATISTIC
@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["admin", "developer", "tester", "manager"])
def get_statistic(request, project_id):
    project = Project.objects.get(id=project_id)
    tasks = project.task_set.all()

    tasks_data = get_data_for_statistics(tasks)

    return render(
        request,
        "projects/statistic.html",
        {
            "project_id": project_id,
            "tasks_data": tasks_data,
        }
    )


# RESTRICTED
@login_required(login_url="/users/login")
def restricted(request):
    return render(request, "projects/restricted.html", {})