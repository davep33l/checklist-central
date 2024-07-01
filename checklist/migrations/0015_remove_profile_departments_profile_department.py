# Generated by Django 4.2.13 on 2024-06-28 10:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0014_remove_taskinstance_processor_notes_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='departments',
        ),
        migrations.AddField(
            model_name='profile',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile_department', to='checklist.department'),
        ),
    ]
