from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import Staff, Hospital, Affiliation
from patients.models import Patient  # À adapter selon ton modèle Patient
from django.db.models import Q

# Vues pour Staff
class StaffDashboardView(LoginRequiredMixin, ListView):
    template_name = 'staff/staff_dashboard.html'
    context_object_name = 'patients'

    def get_queryset(self):
        # Patients gérés par ce staff (via RMS ou Consent)
        return Patient.objects.filter(
            Q(rms_records__created_by=self.request.user.staff) | Q(consents__staff=self.request.user.staff)
        ).distinct()

class StaffDetailView(LoginRequiredMixin, DetailView):
    model = Staff
    template_name = 'staff/staff_detail.html'
    context_object_name = 'staff'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['staff_patients'] = Patient.objects.filter(
            Q(rms_records__created_by=self.object) | Q(consents__staff=self.object)
        ).distinct()
        return context

class StaffPatientListView(LoginRequiredMixin, ListView):
    template_name = 'staff/patient_list.html'
    context_object_name = 'patients'

    def get_queryset(self):
        return Patient.objects.filter(
            Q(rms_records__created_by=self.request.user.staff) | Q(consents__staff=self.request.user.staff)
        ).distinct()

class StaffPatientDetailView(LoginRequiredMixin, DetailView):
    model = Patient
    template_name = 'staff/patient_detail.html'
    context_object_name = 'patient'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient_staffs'] = Staff.objects.filter(
            Q(rms_records__patient=self.object) | Q(consents__patient=self.object)
        ).distinct()
        return context

class StaffCreateView(LoginRequiredMixin, CreateView):
    model = Staff
    template_name = 'staff/staff_form.html'
    fields = ['name', 'first_name', 'sex' , 'type', 'doctor_order_number', 'nurse_order_number', 'student_matricule', 'specialities', 'supervisor', 'phone', 'email']
    success_url = reverse_lazy('staff_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not self.request.user.is_superuser:
            form.errors['__all__'] = form.error_class(["Seul un superuser peut créer un staff."])
        return form

class StaffListView(LoginRequiredMixin, ListView):
    model = Staff
    template_name = 'staff/staff_list.html'
    context_object_name = 'staff_list'

    def get_queryset(self):
        if not self.request.user.is_superuser:
            return Staff.objects.filter(pk=self.request.user.staff.pk)
        return Staff.objects.all()

# Vues pour Hospital
class HospitalDashboardView(LoginRequiredMixin, DetailView):
    model = Hospital
    template_name = 'hospitals/hospital_dashboard.html'
    context_object_name = 'hospital'

    def get_object(self):
        if hasattr(self.request.user, 'hospital'):
            return self.request.user.hospital
        return get_object_or_404(Hospital, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['staff_count'] = self.object.staff_set.count()
        context['patient_count'] = Patient.objects.filter(main_hospital=self.object).count()
        return context

class HospitalDetailView(LoginRequiredMixin, DetailView):
    model = Hospital
    template_name = 'hospitals/hospital_detail.html'
    context_object_name = 'hospital'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['staff_list'] = self.object.staff_set.all()
        context['patient_list'] = Patient.objects.filter(main_hospital=self.object)
        return context

class HospitalListView(LoginRequiredMixin, ListView):
    model = Hospital
    template_name = 'hospitals/hospital_list.html'
    context_object_name = 'hospitals'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Hospital.objects.all()
        elif hasattr(self.request.user, 'hospital'):
            return Hospital.objects.filter(pk=self.request.user.hospital.pk)
        return Hospital.objects.none()

class HospitalCreateView(LoginRequiredMixin, CreateView):
    model = Hospital
    template_name = 'hospitals/hospital_form.html'
    fields = ['user', 'name', 'address', 'phone', 'email']
    success_url = reverse_lazy('hospital_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not self.request.user.is_superuser:
            form.errors['__all__'] = form.error_class(["Seul un superuser peut créer un hôpital."])
        return form

class HospitalStaffListView(LoginRequiredMixin, ListView):
    template_name = 'hospitals/staff_list.html'
    context_object_name = 'staff_list'

    def get_queryset(self):
        hospital = get_object_or_404(Hospital, pk=self.kwargs['pk'])
        return hospital.staff_set.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hospital'] = get_object_or_404(Hospital, pk=self.kwargs['pk'])
        return context

class HospitalPatientListView(LoginRequiredMixin, ListView):
    template_name = 'hospitals/patient_list.html'
    context_object_name = 'patients'

    def get_queryset(self):
        hospital = get_object_or_404(Hospital, pk=self.kwargs['pk'])
        return Patient.objects.filter(main_hospital=hospital)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hospital'] = get_object_or_404(Hospital, pk=self.kwargs['pk'])
        return context