# Generated by Django 4.2.13 on 2024-06-26 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0002_checklisttemplate_team_tasktemplate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasktemplate',
            name='task_template_due_at',
            field=models.TimeField(),
        ),
    ]
