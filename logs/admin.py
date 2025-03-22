from django.contrib import admin
from .models import StaffLogin, ConsultationHistory, RMSHistory

@admin.register(StaffLogin)
class StaffLoginAdmin(admin.ModelAdmin):
    list_display = ('staff', 'login_date', 'ip_address')
    list_filter = ('login_date', 'staff')
    search_fields = ('staff__user__username', 'ip_address')
    ordering = ('-login_date',)  # Plus récent en haut
    list_select_related = ('staff__user',)
    readonly_fields = ('login_date',)  # Non modifiable

@admin.register(ConsultationHistory)
class ConsultationHistoryAdmin(admin.ModelAdmin):
    list_display = ('staff', 'patient', 'rms', 'consultation_date')
    list_filter = ('consultation_date', 'staff', 'patient__main_hospital')
    search_fields = ('staff__user__username', 'patient__num_identifier')
    ordering = ('-consultation_date',)
    list_select_related = ('staff__user', 'patient', 'rms')
    readonly_fields = ('consultation_date',)

@admin.register(RMSHistory)
class RMSHistoryAdmin(admin.ModelAdmin):
    list_display = ('rms', 'modified_by', 'field_changed', 'change_date')
    list_filter = ('change_date', 'modified_by', 'rms__hospital')
    search_fields = ('rms__patient__num_identifier', 'field_changed')
    ordering = ('-change_date',)
    list_select_related = ('rms__patient', 'rms__hospital', 'modified_by__user')
    readonly_fields = ('change_date', 'old_value', 'new_value')