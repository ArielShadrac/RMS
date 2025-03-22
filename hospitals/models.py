# hospitals/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
import uuid
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
        ('nurse', 'Infirmier'),
        ('intern', 'Interne'),
        ('idh', 'Interne Des Hôpitaux'),  # Internes liés à un hôpital
        ('des', 'Docteur En Spécialisation'),  # Ajout des DES
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    num_licence = models.CharField(max_length=100, unique=True, default=uuid.uuid4().hex[:10], blank=True)
    type = models.CharField(max_length=20, choices=STAFF_TYPES, default='doctor')
    specialities = models.ManyToManyField(Speciality, blank=True)
    hospitals = models.ManyToManyField(Hospital, through='Affiliation')
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(unique=True)
    supervisor = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)  # Pour internes, IDH, DES
    def __str__(self):
        return f"{self.user.username} ({self.get_type_display()})"
    
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
    if instance.pk:  # Si l'instance existe déjà (mise à jour)
        old_instance = Staff.objects.get(pk=instance.pk)
        if old_instance.type != instance.type:  # Si le type change
            StaffStatusHistory.objects.create(
                staff=instance,
                old_type=old_instance.type,
                new_type=instance.type
            )
            # Si devient 'doctor' ou 'des', ajuster le superviseur
            if instance.type in ['doctor', 'des']:
                instance.supervisor = None  # Plus besoin de superviseur pour DES ou médecin