# Generated by Django 4.1.4 on 2023-11-16 07:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_skillcategory_skills_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='skillcategory',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subcategories', to='main.skillcategory'),
        ),
    ]
