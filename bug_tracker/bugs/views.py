from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required  # auth


# Create your views here.
#@login_required(login_url="/login")
def index(request):
    return HttpResponse("Bugs list")


#@login_required(login_url="/login")
def create(request):
    return HttpResponse("Create bug")


#@login_required(login_url="/login")
def update(request, id):
    return HttpResponse("Update bug")


#@login_required(login_url="/login")
def delete(request, id):
    return HttpResponse("Delete bug")