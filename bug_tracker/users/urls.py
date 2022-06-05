from django.urls import path
from . import views

# Routing in users app
urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.sign_in, name="sign_in"),
    path("logout/", views.log_out, name="log_out")
]
