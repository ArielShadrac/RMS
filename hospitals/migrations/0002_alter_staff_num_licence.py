# Generated by Django 4.2.18 on 2025-03-22 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hospitals", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="staff",
            name="num_licence",
            field=models.CharField(
                blank=True, default="301e9c7f5d", max_length=100, unique=True
            ),
        ),
    ]
