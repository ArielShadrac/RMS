from django.contrib import admin
from django.db.models import Count
from .models import Speciality, Hospital, Staff, Affiliation, StaffStatusHistory

# Admin pour Speciality
@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

# Inline pour Affiliation
class AffiliationInline(admin.TabularInline):
    model = Affiliation
    extra = 1
    fields = ('hospital', 'staff', 'status', 'role', 'date_start', 'date_end')
    autocomplete_fields = ('staff', 'hospital')
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('staff__user', 'hospital')

# Inline pour StaffStatusHistory
class StatusHistoryInline(admin.TabularInline):
    model = StaffStatusHistory
    extra = 0
    fields = ('old_type', 'new_type', 'change_date')
    readonly_fields = ('old_type', 'new_type', 'change_date')
    can_delete = False

# Admin pour Hospital
@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone', 'email', 'user')
    search_fields = ('name', 'address', 'email', 'phone')
    list_filter = ('name',)
    ordering = ('name',)
    inlines = [AffiliationInline]
    list_select_related = ('user',)
    fieldsets = (
        (None, {
            'fields': ('user', 'name', 'address', 'phone', 'email')
        }),
    )
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['phone'].required = True
        form.base_fields['email'].required = True
        return form

# Admin pour Staff
@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('username', 'type', 'get_identifier', 'email', 'phone', 'supervisor_name', 'hospital_count')
    list_filter = ('type', 'hospitals')
    search_fields = ('user__username', 'email', 'doctor_order_number', 'nurse_order_number', 'student_matricule', 'phone')
    ordering = ('user__username',)
    inlines = [AffiliationInline, StatusHistoryInline]
    autocomplete_fields = ('supervisor',)
    actions = ['promote_to_doctor', 'promote_to_des']
    list_per_page = 50
    list_select_related = ('user', 'supervisor', 'supervisor__user')
    list_prefetch_related = ('hospitals', 'specialities')
    fieldsets = (
        (None, {
            'fields': ('user', 'type', 'doctor_order_number', 'nurse_order_number', 'student_matricule', 'specialities', 'supervisor', 'phone', 'email')
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(hospital_count=Count('hospitals'))

    def username(self, obj):
        return obj.user.username
    username.short_description = "Nom d’utilisateur"

    def supervisor_name(self, obj):
        return obj.supervisor.user.username if obj.supervisor else "Aucun"
    supervisor_name.short_description = "Superviseur"

    def hospital_count(self, obj):
        return obj.hospital_count
    hospital_count.short_description = "Nb Hôpitaux"

    def promote_to_doctor(self, request, queryset):
        if not request.user.is_superuser:
            self.message_user(request, "Action réservée aux superusers.", level='error')
            return
        updated = queryset.exclude(type='doctor').update(type='doctor', supervisor=None)
        self.message_user(request, f"{updated} membre(s) promu(s) en médecin.")

    def promote_to_des(self, request, queryset):
        if not request.user.is_superuser:
            self.message_user(request, "Action réservée aux superusers.", level='error')
            return
        updated = queryset.exclude(type__in=['des', 'doctor']).update(type='des')
        self.message_user(request, f"{updated} membre(s) promu(s) en DES.")

# Admin pour Affiliation
@admin.register(Affiliation)
class AffiliationAdmin(admin.ModelAdmin):
    list_display = ('staff', 'hospital', 'status', 'role', 'date_start', 'date_end')
    list_filter = ('status', 'role', 'hospital')
    search_fields = ('staff__user__username', 'hospital__name')
    autocomplete_fields = ('staff', 'hospital')
    list_select_related = ('staff__user', 'hospital')

# Admin pour StaffStatusHistory
@admin.register(StaffStatusHistory)
class StaffStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ('staff', 'old_type', 'new_type', 'change_date')
    list_filter = ('old_type', 'new_type')
    search_fields = ('staff__user__username',)
    readonly_fields = ('staff', 'old_type', 'new_type', 'change_date')
    can_delete = False