from .base import *

ALLOWED_HOSTS = ["*"]

TIME_ZONE = "Europe/Kiev"

LOGIN_REDIRECT_URL = "/"

INSTALLED_APPS += (
    "users.apps.UsersConfig",
    "projects.apps.ProjectsConfig",
    "crispy_forms",
)

TEMPLATES[0]["DIRS"] = [BASE_DIR / "templates"]

STATICFILES_DIRS = [
    "./bug_tracker/static",
]

CRISPY_TEMPLATE_PACK = "bootstrap4"