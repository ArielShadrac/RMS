# Generated by Django 4.2.18 on 2025-03-22 15:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Affiliation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "En attente"),
                            ("accepted", "Accepté"),
                            ("rejected", "Refusé"),
                        ],
                        default="pending",
                        max_length=20,
                    ),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("doctor", "Médecin"),
                            ("nurse", "Infirmier"),
                            ("intern", "Interne"),
                            ("idh", "IDH"),
                            ("des", "DES"),
                            ("admin", "Administrateur"),
                            ("assistant", "Assistant"),
                        ],
                        default="doctor",
                        max_length=20,
                    ),
                ),
                ("date_start", models.DateField()),
                ("date_end", models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Hospital",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("address", models.TextField()),
                ("phone", models.CharField(max_length=15, unique=True)),
                ("email", models.EmailField(max_length=254, unique=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Speciality",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Staff",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "num_licence",
                    models.CharField(
                        blank=True, default="d1df9bf0b4", max_length=100, unique=True
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("doctor", "Médecin"),
                            ("nurse", "Infirmier"),
                            ("intern", "Interne"),
                            ("idh", "Interne Des Hôpitaux"),
                            ("des", "Docteur En Spécialisation"),
                        ],
                        default="doctor",
                        max_length=20,
                    ),
                ),
                ("phone", models.CharField(blank=True, max_length=15)),
                ("email", models.EmailField(max_length=254, unique=True)),
                (
                    "hospitals",
                    models.ManyToManyField(
                        through="hospitals.Affiliation", to="hospitals.hospital"
                    ),
                ),
                (
                    "specialities",
                    models.ManyToManyField(blank=True, to="hospitals.speciality"),
                ),
                (
                    "supervisor",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="hospitals.staff",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="StaffStatusHistory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "old_type",
                    models.CharField(
                        choices=[
                            ("doctor", "Médecin"),
                            ("nurse", "Infirmier"),
                            ("intern", "Interne"),
                            ("idh", "Interne Des Hôpitaux"),
                            ("des", "Docteur En Spécialisation"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "new_type",
                    models.CharField(
                        choices=[
                            ("doctor", "Médecin"),
                            ("nurse", "Infirmier"),
                            ("intern", "Interne"),
                            ("idh", "Interne Des Hôpitaux"),
                            ("des", "Docteur En Spécialisation"),
                        ],
                        max_length=20,
                    ),
                ),
                ("change_date", models.DateTimeField(auto_now_add=True)),
                (
                    "staff",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="hospitals.staff",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="affiliation",
            name="hospital",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="hospitals.hospital"
            ),
        ),
        migrations.AddField(
            model_name="affiliation",
            name="staff",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="hospitals.staff"
            ),
        ),
    ]
