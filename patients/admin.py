# patients/admin.py
from django.contrib import admin
from .models import Patient, RMS, Consent

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('num_identifier', 'first_name', 'last_name', 'birth_date', 'birth_year_approx', 'age_in_days', 'estimated_age', 'get_age', 'main_hospital')
    search_fields = ('num_identifier', 'first_name', 'last_name')
    list_filter = ('main_hospital',)
    ordering = ('last_name', 'first_name')
    list_select_related = ('main_hospital',)
    fieldsets = (
        (None, {
            'fields': ('num_identifier', 'first_name', 'last_name', 'birth_date', 'birth_year_approx', 'age_in_days', 'estimated_age', 'main_hospital', 'phone', 'email', 'fhir_data')
        }),
    )
    readonly_fields = ('num_identifier',)  # Non modifiable

@admin.register(RMS)
class RMSAdmin(admin.ModelAdmin):
    list_display = ('patient', 'hospital', 'created_by', 'updated_by', 'updated_at')
    search_fields = ('patient__num_identifier', 'hospital__name')
    list_filter = ('hospital', 'created_by', 'updated_at')
    list_select_related = ('patient', 'hospital', 'created_by__user', 'updated_by__user')
    autocomplete_fields = ('patient', 'hospital', 'created_by', 'updated_by')

@admin.register(Consent)
class ConsentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'hospital', 'staff', 'agreed', 'consent_date', 'expiry_date')
    list_filter = ('agreed', 'hospital')
    search_fields = ('patient__num_identifier', 'hospital__name')
    list_select_related = ('patient', 'hospital', 'staff__user')
    autocomplete_fields = ('patient', 'hospital', 'staff')