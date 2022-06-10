from django.urls import path
from . import views

# Routing in projects app
urlpatterns = [
    # Projects URL
    path("",
         views.read_projects,
         name="read_projects"),
    path("create/",
         views.create_project,
         name="create_projects"),
    path("update/<int:project_id>",
         views.update_project,
         name="update_projects"),
    path("delete/<int:project_id>",
         views.delete_project,
         name="delete_project"),
    path("allow_access/<int:project_id>",
         views.allow_access,
         name="allow_access"),
    path("deny_access/<int:project_id>/<int:user_id>",
         views.deny_access,
         name="deny_access"),
    path("dashboard/<int:project_id>",
         views.dashboard,
         name="dashboard"),

    # Tasks
    path("tasks/<int:project_id>",
         views.read_tasks,
         name="read_tasks"),
    path("task/<int:project_id>/<int:task_id>",
         views.read_task,
         name="read_task"),
    path("add_task/<int:project_id>",
         views.add_task,
         name="add_task"),
    path("update_task/<int:project_id>/<int:task_id>",
         views.update_task,
         name="update_task"),
    path("delete_task/<int:project_id>/<int:task_id>",
         views.delete_task,
         name="delete_task"),
    path("add_task_to_dashboard/<int:project_id>/<int:task_id>",
         views.add_task_to_dashboard,
         name="add_task_to_dashboard"),
    path("delete_task_from_dashboard/<int:project_id>/<int:task_id>",
         views.delete_task_from_dashboard,
         name="delete_task_from_dashboard"),
    path("load_tasks_in_csv/<int:project_id>",
         views.load_tasks_in_csv,
         name="load_tasks_in_csv"),


    # Bugs
    path("bugs/<int:id>",
         views.read_bugs,
         name="read_bugs"),

    # Statistics
    path("statistic/<int:id>",
         views.get_statistic,
         name="statistic"),

    # Restricted
    path("restricted/",
         views.restricted,
         name="restricted"),
]
