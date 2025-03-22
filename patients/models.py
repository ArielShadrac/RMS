from django.db import models
from django.db.models import JSONField
import uuid
from datetime import date
from hospitals.models import Hospital, Staff
class Patient(models.Model):
    num_identifier = models.CharField(max_length=20, unique=True, default=uuid.uuid4().hex[:12], editable=False, verbose_name="Numéro d'identification")  # Généré automatiquement
    last_name = models.CharField(max_length=100, blank=False, verbose_name="Nom de famille")
    first_name = models.CharField(max_length=250, blank=False, verbose_name="Prénom(s)")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Date de naissance")
    birth_year_approx = models.PositiveIntegerField(null=True, blank=True, verbose_name="Année approximative de naissance  (ex. : né vers 1995)")
    age_in_days = models.PositiveIntegerField(null=True, blank=True, verbose_name="Âge en jours pour bébés de moins de 2 ans")
    estimated_age = models.PositiveIntegerField(null=True, blank=True, verbose_name="Âge estimé en années si rien d'autre") 
    main_hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True, blank=True, related_name='patients', verbose_name="Hôpital")
    phone = models.CharField(max_length=15, blank=True, verbose_name="Numéro de téléphone")
    email = models.EmailField(blank=True, verbose_name="Adresse e-mail")
    fhir_data = JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.num_identifier})"

    def get_age(self):
        """Calcule l'âge en fonction des données disponibles."""
        today = date.today()
        if self.birth_date:  # Date exacte connue
            delta = today - self.birth_date
            days = delta.days
            if days <= 30:  # Moins de 30 jours → en jours
                return f"{days} jour{'s' if days > 1 else ''}"
            elif days <= 730:  # Moins de 2 ans → en mois
                months = days // 30
                return f"{months} mois"
            else:  # Plus de 2 ans → en années
                years = today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
                return f"{years} ans"
        elif self.age_in_days is not None:  # Âge en jours spécifié
            if self.age_in_days <= 30:
                return f"{self.age_in_days} jour{'s' if self.age_in_days > 1 else ''}"
            elif self.age_in_days <= 730:
                months = self.age_in_days // 30
                return f"{months} mois"
            else:
                years = self.age_in_days // 365
                return f"{years} ans"
        elif self.birth_year_approx:  # Année approximative
            approx_age = today.year - self.birth_year_approx
            return f"~{approx_age} ans"
        elif self.estimated_age:  # Âge estimé
            return f"~{self.estimated_age} ans"
        return "Inconnu"
    get_age.short_description = "Âge"

        

class RMS(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='rms_records', verbose_name="Patient")
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='rms_records', verbose_name="Hôpital")
    created_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='rms_created', verbose_name="Créé par")
    updated_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='rms_updated', verbose_name="Mis à jour par")
    fhir_data = JSONField(default=dict, verbose_name="Données FHIR")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de mise à jour")

    class Meta:
        verbose_name = "RMS"
        verbose_name_plural = "RMS"

    def __str__(self):
        return f"RMS de {self.patient} - {self.hospital} ({self.updated_at})"

class Consent(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='consents')
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='consents')
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='consents_granted')
    agreed = models.BooleanField(default=False)
    consent_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Consentement"
        verbose_name_plural = "Consentements"

    def __str__(self):
        return f"Consentement de {self.patient} pour {self.hospital} ({'Oui' if self.agreed else 'Non'})"