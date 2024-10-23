# Generated by Django 4.2.16 on 2024-10-19 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0006_incident_prioridad'),
    ]

    operations = [
        migrations.AddField(
            model_name='incident',
            name='category',
            field=models.CharField(blank=True, choices=[('RENDIMIENTO', 'Rendimiento'), ('UI', 'UI'), ('DOCUMENTACION', 'Documentación'), ('APIS', 'API’s'), ('BASEDATOS', 'Bases de datos'), ('SEGURIDAD', 'Seguridad'), ('DEPENDENCIAS', 'Dependencias de terceros')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='incident',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='files/'),
        ),
        migrations.AlterField(
            model_name='incident',
            name='incident_text',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
