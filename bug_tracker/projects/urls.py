from django.urls import path
from . import views

# Routing in projects app
urlpatterns = [
    path('', views.index, name="index"),
    path('create/', views.create, name="create"),
    path('update/<int:id>', views.update, name="update"),
    path('delete/<int:id>', views.delete, name="delete"),
    path('access/<int:id>', views.manage_access, name="allow_access"),
    path('access/deny/<int:project_id>/<int:user_id>', views.deny_access, name="deny_access"),
    path('restricted/', views.restricted, name="restricted"),
]
