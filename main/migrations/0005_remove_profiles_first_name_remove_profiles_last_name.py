# Generated by Django 4.1.4 on 2023-11-04 07:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_profiles_first_name_profiles_last_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profiles',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='profiles',
            name='last_name',
        ),
    ]
