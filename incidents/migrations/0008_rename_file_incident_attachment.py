# Generated by Django 4.2.16 on 2024-10-19 00:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0007_incident_category_incident_file_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='incident',
            old_name='file',
            new_name='attachment',
        ),
    ]
