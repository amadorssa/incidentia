# Generated by Django 5.1.2 on 2024-10-26 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0002_alter_incident_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='incident',
            name='attachment',
            field=models.FileField(blank=True, null=True, upload_to='media/'),
        ),
        migrations.AddField(
            model_name='incident',
            name='category',
            field=models.CharField(blank=True, choices=[('RENDIMIENTO', 'Rendimiento'), ('UI', 'UI'), ('DOCUMENTACION', 'Documentación'), ('APIS', 'API’s'), ('BASEDATOS', 'Bases de datos'), ('SEGURIDAD', 'Seguridad'), ('DEPENDENCIAS', 'Dependencias de terceros')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='incident',
            name='due_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Fecha de vencimiento'),
        ),
        migrations.AddField(
            model_name='incident',
            name='prioridad',
            field=models.CharField(choices=[('BAJA', 'Baja'), ('MEDIA', 'Media'), ('ALTA', 'Alta'), ('CRITICA', 'Crítica')], default='MEDIA', max_length=7),
        ),
        migrations.AddField(
            model_name='incident',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Fecha de inicio'),
        ),
        migrations.AlterField(
            model_name='incident',
            name='incident_text',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
