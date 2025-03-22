from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

class Speciality(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Spécialité"
        verbose_name_plural = "Spécialités"

class Hospital(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=15, blank=False, unique=True)
    email = models.EmailField(unique=True, blank=False)
    def __str__(self):
        return f"{self.name} ({self.address[:20]}...)"
    
    class Meta:
        verbose_name = "Hôpital"
        verbose_name_plural = "Hôpitaux"

class Staff(models.Model):
    STAFF_TYPES = [
        ('doctor', 'Médecin'),
        ('des', 'Docteur En Spécialisation'),
        ('idh', 'Interne Des Hôpitaux'),
        ('intern', 'Interne'),
        ('nurse', 'Infirmier'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=STAFF_TYPES, default='doctor')
    doctor_order_number = models.CharField(max_length=100, unique=True, blank=True, null=True)  # Numéro d’ordre médecin
    nurse_order_number = models.CharField(max_length=100, unique=True, blank=True, null=True)  # Numéro d’ordre infirmier
    student_matricule = models.CharField(max_length=100, unique=True, blank=True, null=True)  # Matricule étudiant
    specialities = models.ManyToManyField(Speciality, blank=True)
    hospitals = models.ManyToManyField(Hospital, through='Affiliation')
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(unique=True)
    supervisor = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return f"{self.user.username} ({self.get_type_display()})"

    def get_identifier(self):
        """Retourne l’identifiant selon le type."""
        if self.type == 'doctor':
            return self.doctor_order_number or "Non défini"
        elif self.type == 'nurse':
            return self.nurse_order_number or "Non défini"
        elif self.type in ['intern', 'idh', 'des']:
            return self.student_matricule or "Non défini"
        return "Inconnu"

    def clean(self):
        """Validation personnalisée selon le type."""
        if self.type == 'doctor' and not self.doctor_order_number:
            raise ValidationError("Un médecin doit avoir un numéro d’ordre délivré par l’Ordre des Médecins.")
        elif self.type == 'nurse' and not self.nurse_order_number:
            raise ValidationError("Un infirmier doit avoir un numéro d’ordre délivré par l’Ordre des Infirmiers.")
        elif self.type in ['intern', 'idh', 'des'] and not self.student_matricule:
            raise ValidationError("Un interne, IDH ou DES doit avoir un matricule délivré par l’administration.")
        # Vérifie qu’un seul identifiant est rempli
        identifiers = [self.doctor_order_number, self.nurse_order_number, self.student_matricule]
        if sum(1 for x in identifiers if x) > 1:
            raise ValidationError("Un seul identifiant (numéro d’ordre ou matricule) doit être défini.")

    class Meta:
        verbose_name = "Personnel"
        verbose_name_plural = "Personnel"

class Affiliation(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('pending', 'En attente'), ('accepted', 'Accepté'), ('rejected', 'Refusé')], default='pending')
    role = models.CharField(max_length=20, choices=[('doctor', 'Médecin'), ('nurse', 'Infirmier'), ('intern', 'Interne'), ('idh', 'IDH'), ('des', 'DES'), ('admin', 'Administrateur'), ('assistant', 'Assistant')], default='doctor')
    date_start = models.DateField()
    date_end = models.DateField(null=True, blank=True)
    def __str__(self):
        return f"{self.staff.user.username} - {self.hospital.name} ({self.role})"
    
    class Meta:
        verbose_name = "Affiliation"
        verbose_name_plural = "Affiliations"

class StaffStatusHistory(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    old_type = models.CharField(max_length=20, choices=Staff.STAFF_TYPES)
    new_type = models.CharField(max_length=20, choices=Staff.STAFF_TYPES)
    change_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.staff.user.username}: {self.old_type} → {self.new_type} ({self.change_date})"
    
    class Meta:
        verbose_name = "Historique des statuts"
        verbose_name_plural = "Historique des statuts"

# Signal pour suivre les transitions de statut
@receiver(pre_save, sender=Staff)
def track_status_change(sender, instance, **kwargs):
    if instance.pk:  # Si l’instance existe déjà (mise à jour)
        old_instance = Staff.objects.get(pk=instance.pk)
        if old_instance.type != instance.type:  # Si le type change
            StaffStatusHistory.objects.create(
                staff=instance,
                old_type=old_instance.type,
                new_type=instance.type
            )
            # Supprimer le superviseur uniquement pour 'doctor'
            if instance.type == 'doctor':
                instance.supervisor = None