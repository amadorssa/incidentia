# Generated by Django 5.1.2 on 2024-10-30 03:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0005_incident_organizacion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='incident',
            name='organizacion',
        ),
    ]