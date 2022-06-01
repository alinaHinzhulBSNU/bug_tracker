from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required  # auth


# Create your views here.
#@login_required(login_url="/login")
def index(request):
    return HttpResponse("Projects list")


#@login_required(login_url="/login")
def create(request):
    return HttpResponse("Create project")


#@login_required(login_url="/login")
def update(request, id):
    return HttpResponse("Update project")


#@login_required(login_url="/login")
def delete(request, id):
    return HttpResponse("Delete project")