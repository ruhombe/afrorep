# Generated by Django 4.1.4 on 2023-11-14 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_alter_portfolio_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='profiles',
            name='bio',
            field=models.TextField(blank=True, max_length=4000, null=True),
        ),
    ]
