from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Project
from .decorators import allowed_users
from .helpers import get_status_by_value
from .analytics import get_data_for_statistics


# DASHBOARD
@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["developer", "tester", "manager"])
def dashboard(request, project_id):
    project = Project.objects.get(id=project_id)

    to_do_tasks = project.task_set.filter(status=get_status_by_value("to do"))
    to_do_bugs = project.bug_set.filter(status=get_status_by_value("to do"))

    doing_tasks = project.task_set.filter(status=get_status_by_value("doing"))
    doing_bugs = project.bug_set.filter(status=get_status_by_value("doing"))

    done_tasks = project.task_set.filter(status=get_status_by_value("done"))
    done_bugs = project.bug_set.filter(status=get_status_by_value("done"))

    return render(
        request,
        "projects/dashboard.html",
        {
            "project_id": project_id,
            "to_do_tasks": to_do_tasks,
            "to_do_bugs": to_do_bugs,
            "doing_tasks": doing_tasks,
            "doing_bugs": doing_bugs,
            "done_tasks": done_tasks,
            "done_bugs": done_bugs,
        }
    )


# STATISTIC
@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["developer", "tester", "manager"])
def get_tasks_statistic(request, project_id):
    project = Project.objects.get(id=project_id)
    tasks = project.task_set.all()

    data = get_data_for_statistics(tasks)
    description = "Tasks statistic"
    label = "Tasks"

    return render(
        request,
        "projects/statistic.html",
        {
            "project_id": project_id,
            "data": data,
            "description": description,
            "label": label,
        }
    )


@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["developer", "tester", "manager"])
def get_bugs_statistic(request, project_id):
    project = Project.objects.get(id=project_id)
    bugs = project.bug_set.all()

    data = get_data_for_statistics(bugs)
    description = "Bugs statistic"
    label = "Bugs"

    return render(
        request,
        "projects/statistic.html",
        {
            "project_id": project_id,
            "data": data,
            "description": description,
            "label": label,
        }
    )


# RESTRICTED
@login_required(login_url="/users/login")
def restricted(request):
    return render(request, "projects/restricted.html", {})
