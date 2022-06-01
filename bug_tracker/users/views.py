from django.shortcuts import render, redirect
from django.http import HttpResponse


# REGISTER NEW USER
def register(request):
    return HttpResponse("Register")