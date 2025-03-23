from django.urls import path
from . import views

urlpatterns = [
    # Staff URLs
    path('staff/dashboard/', views.StaffDashboardView.as_view(), name='staff_dashboard'),
    path('staff/<int:pk>/', views.StaffDetailView.as_view(), name='staff_detail'),
    path('staff/patients/', views.StaffPatientListView.as_view(), name='staff_patient_list'),
    path('staff/patients/<int:pk>/', views.StaffPatientDetailView.as_view(), name='staff_patient_detail'),
    path('staff/create/', views.StaffCreateView.as_view(), name='staff_create'),
    path('staff/list/', views.StaffListView.as_view(), name='staff_list'),
    
    # Hospital URLs
    path('hospitals/dashboard/<int:pk>/', views.HospitalDashboardView.as_view(), name='hospital_dashboard'),
    path('hospitals/<int:pk>/', views.HospitalDetailView.as_view(), name='hospital_detail'),
    path('hospitals/', views.HospitalListView.as_view(), name='hospital_list'),
    path('hospitals/create/', views.HospitalCreateView.as_view(), name='hospital_create'),
    path('hospitals/<int:pk>/staff/', views.HospitalStaffListView.as_view(), name='hospital_staff_list'),
    path('hospitals/<int:pk>/patients/', views.HospitalPatientListView.as_view(), name='hospital_patient_list'),
]