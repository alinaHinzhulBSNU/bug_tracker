from django.urls import path
from . import views

# Routing in users app
urlpatterns = [
    path('create/', views.register, name='register'),
]