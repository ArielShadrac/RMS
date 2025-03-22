from django.urls import path
from . import views

urlpatterns = [
    path("login_logs", views.login_logs, name="login_logs"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
]