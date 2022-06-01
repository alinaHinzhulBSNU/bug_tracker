from .base import *

LANGUAGE_CODE = 'uk-ua'
TIME_ZONE = 'Europe/Kiev'

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/login/"

INSTALLED_APPS += (
    "profiles.apps.ProfilesConfig",
    "bugs.apps.BugsConfig",
    "tasks.apps.TasksConfig",
    "projects.apps.ProjectsConfig",
)