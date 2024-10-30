# Generated by Django 5.1.2 on 2024-10-30 02:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0004_alter_incident_user_creator'),
        ('organizaciones', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='incident',
            name='organizacion',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='incidentes', to='organizaciones.organizacion'),
        ),
    ]