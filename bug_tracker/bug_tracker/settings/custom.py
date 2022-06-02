from .base import *

TIME_ZONE = 'Europe/Kiev'

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/login/"

INSTALLED_APPS += (
    "users.apps.UsersConfig",
    "projects.apps.ProjectsConfig",
)

TEMPLATES[0]['DIRS'] = [BASE_DIR / 'templates']

STATICFILES_DIRS = [
    "./bug_tracker/static",
]