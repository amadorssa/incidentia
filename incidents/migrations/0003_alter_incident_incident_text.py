# Generated by Django 5.1.2 on 2024-11-15 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0002_incident_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident',
            name='incident_text',
            field=models.CharField(blank=True, default='nombre', max_length=200),
        ),
    ]