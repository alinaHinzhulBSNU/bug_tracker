from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required  # auth


# Create your views here.
#@login_required(login_url="/login")
def index(request):
    return render(request, "bugs/home.html", {})


#@login_required(login_url="/login")
def create(request):
    return render(request, "bugs/form.html", {})


#@login_required(login_url="/login")
def update(request, id):
    return render(request, "bugs/form.html", {})


#@login_required(login_url="/login")
def delete(request, id):
    return redirect(index)