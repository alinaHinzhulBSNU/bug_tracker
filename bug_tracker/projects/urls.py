from django.urls import path
from . import views

# Routing in projects app
urlpatterns = [
    # Projects
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("update/<int:id>", views.update, name="update"),
    path("delete/<int:id>", views.delete, name="delete"),
    path("allow_access/<int:id>", views.allow_access, name="allow_access"),
    path("deny_access/<int:project_id>/<int:user_id>", views.deny_access, name="deny_access"),
    path("dashboard/<int:id>", views.dashboard, name="dashboard"),

    # Tasks
    path("tasks/<int:id>", views.tasks, name="tasks"),
    path("add_task/<int:id>", views.add_task, name="add_task"),
    path("delete_task/<int:project_id>/<int:task_id>", views.delete_task, name="delete_task"),
    path("update_task/<int:project_id>/<int:task_id>", views.update_task, name="update_task"),
    path("add_to_dashboard/<int:project_id>/<int:task_id>", views.add_to_dashboard, name="add_to_dashboard"),
    path("delete_from_dashboard/<int:project_id>/<int:task_id>", views.delete_from_dashboard, name="add_to_dashboard"),

    # Restricted
    path("restricted/", views.restricted, name="restricted"),
]
