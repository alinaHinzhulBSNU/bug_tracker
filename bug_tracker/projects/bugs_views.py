import datetime
import csv

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .decorators import allowed_users
from .forms import BugForm
from .models import Project, Bug
from .helpers import get_status_by_value
from .analytics import predict_time_for_item_by_ml


# CRUD
@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["developer", "tester", "manager"])
def read_bugs(request, project_id):
    project = Project.objects.get(id=project_id)
    return render(request, "projects/bugs.html", {"project": project})


@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["developer", "tester", "manager"])
def read_bug(request, project_id, bug_id):
    bug = Bug.objects.get(id=bug_id)

    return render(
        request,
        "projects/bug.html",
        {
            "prediction": "",
            "bug": bug,
            "project_id": project_id,
        }
    )


@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["manager"])
def create_bug(request, project_id):
    project = Project.objects.get(id=project_id)

    if request.POST:
        form = BugForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/bugs/" + str(project_id))
    else:
        form = BugForm(project=project, status=get_status_by_value("backlog"))

    return render(
        request,
        "projects/bug_form.html",
        {
            "form": form,
            "project": project,
        }
    )


@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["manager"])
def update_bug(request, project_id, bug_id):
    bug = Bug.objects.get(id=bug_id)

    if request.POST:
        form = BugForm(data=request.POST, files=request.FILES, instance=bug)
        if form.is_valid():
            form.save()
            return redirect("/bugs/" + str(project_id))
    else:
        form = BugForm(instance=bug)

    return render(
        request,
        "projects/bug_form.html",
        {
            "form": form,
        }
    )


@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["manager"])
def delete_bug(request, project_id, bug_id):
    Bug.objects.get(id=bug_id).delete()
    return redirect("/bugs/" + str(project_id))


# DISPLAY OR HIDE ON DASHBOARD
@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["developer", "tester", "manager"])
def add_bug_to_dashboard(request, project_id, bug_id):
    bug = Bug.objects.get(id=bug_id)

    bug.status = get_status_by_value("to do")
    bug.start_time = datetime.datetime.now()

    bug.save()

    return redirect("/bugs/" + str(project_id))


@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["developer", "tester", "manager"])
def delete_bug_from_dashboard(request, project_id, bug_id):
    bug = Bug.objects.get(id=bug_id)

    bug.status = get_status_by_value("backlog")
    bug.start_time = None
    bug.end_time = None

    bug.save()

    return redirect("/bugs/" + str(project_id))


# CHANGE STATUS
@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["developer", "tester", "manager"])
def set_bug_to_do(request, project_id, bug_id):
    bug = Bug.objects.get(id=bug_id)

    bug.status = get_status_by_value("to do")
    bug.start_time = datetime.datetime.now()
    bug.end_time = None

    bug.save()

    return redirect("/dashboard/" + str(project_id))


@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["developer", "tester", "manager"])
def set_bug_doing(request, project_id, bug_id):
    bug = Bug.objects.get(id=bug_id)

    bug.status = get_status_by_value("doing")
    bug.end_time = None

    bug.save()

    return redirect("/dashboard/" + str(project_id))


@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["developer", "tester", "manager"])
def set_bug_done(request, project_id, bug_id):
    bug = Bug.objects.get(id=bug_id)

    bug.status = get_status_by_value("done")
    bug.end_time = datetime.datetime.now()

    bug.save()

    return redirect("/dashboard/" + str(project_id))


# CSV LOADING
@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["developer", "tester", "manager"])
def load_bugs_in_csv(request, project_id):
    project = Project.objects.get(id=project_id)

    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="bugs.csv"'},
    )

    writer = csv.writer(response)
    for bug in project.bug_set.all():
        writer.writerow([bug.id,
                         bug.summary,
                         bug.description,
                         bug.get_reproducibility(),
                         bug.get_severity(),
                         bug.get_priority(),
                         bug.get_symptom(),
                         bug.workaround,
                         bug.start_time,
                         bug.end_time,
                         bug.get_status(),
                         bug.performer.username,
                         bug.project.name,
                         ])

    return response


# ML PREDICTION
@login_required(login_url="/users/login")
@allowed_users(allowed_roles=["developer", "tester", "manager"])
def predict_for_bug(request, project_id, bug_id):
    bug = Bug.objects.get(id=bug_id)

    project = Project.objects.get(id=project_id)
    bugs = project.bug_set.filter(status=get_status_by_value("done"))

    prediction = predict_time_for_item_by_ml(
        performer=bug.performer,
        severity=bug.severity,
        items=bugs
    )

    return render(request,
                  "projects/bug.html",
                  {"prediction": prediction,
                   "bug": bug,
                   "project_id": project_id})
