from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("hospital_list", views.hospital_list, name="hospital_list"),
    path("staff_list", views.staff_list, name="staff_list"),
]