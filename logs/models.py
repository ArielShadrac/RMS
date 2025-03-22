from django.db import models
from django.db.models import JSONField
from hospitals.models import Staff
from patients.models import Patient, RMS

class StaffLogin(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='logins', verbose_name="Personnel")
    login_date = models.DateTimeField(auto_now_add=True, verbose_name="Date de connexion")
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="Adresse IP")

    def __str__(self):
        return f"{self.staff.user.username} - {self.login_date}"

    class Meta:
        verbose_name = "Connexion du personnel"
        verbose_name_plural = "Connexions du personnel"

class ConsultationHistory(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='consultations', verbose_name="Personnel")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='consultations', verbose_name="Patient")
    rms = models.ForeignKey(RMS, on_delete=models.CASCADE, null=True, blank=True, related_name='consultations', verbose_name="RMS")
    consultation_date = models.DateTimeField(auto_now_add=True, verbose_name="Date de consultation")

    def __str__(self):
        return f"{self.staff.user.username} - {self.patient} - {self.consultation_date}"

    class Meta:
        verbose_name = "Historique de consultation"
        verbose_name_plural = "Historique des consultations"

class RMSHistory(models.Model):
    rms = models.ForeignKey(RMS, on_delete=models.CASCADE, related_name='history', verbose_name="RMS")
    modified_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='rms_modifications', verbose_name="Modifié par")
    field_changed = models.CharField(max_length=100, verbose_name="Champ modifié")
    old_value = JSONField(null=True, blank=True, verbose_name="Ancienne valeur")
    new_value = JSONField(null=True, blank=True, verbose_name="Nouvelle valeur")
    change_date = models.DateTimeField(auto_now_add=True, verbose_name="Date de modification")

    def __str__(self):
        return f"{self.rms} - {self.field_changed} - {self.change_date}"

    class Meta:
        verbose_name = "Historique RMS"
        verbose_name_plural = "Historique RMS"