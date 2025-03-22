from django.shortcuts import render
from django.http import HttpResponse
from .models import Hospital, Staff, Speciality, Affiliation, StaffStatusHistory
# Create your views here. 

def index(request):
    return render(request, "index.html")

def hospital_list(request):
    return render(request, "hospital/hospital_list.html")

def staff_list(request):
    return render(request, "staff/staff_list.html")