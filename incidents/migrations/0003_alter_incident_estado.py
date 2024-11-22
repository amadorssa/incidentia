# Generated by Django 4.2.5 on 2024-11-20 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0002_incident_usuario_modificador_historialincidente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident',
            name='estado',
            field=models.CharField(choices=[('ABIERTO', 'Abierto'), ('EN_PROGRESO', 'En progreso'), ('RESUELTO', 'Resuleto'), ('DESCARTADO', 'Descartado')], default='nuevo', max_length=20),
        ),
    ]