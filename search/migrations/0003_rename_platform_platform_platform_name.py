# Generated by Django 5.1.2 on 2024-11-08 18:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0002_platform'),
    ]

    operations = [
        migrations.RenameField(
            model_name='platform',
            old_name='platform',
            new_name='platform_name',
        ),
    ]