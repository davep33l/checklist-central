from django.db import models

# import user
from django.contrib.auth.models import User


# Create your models here.

class Department(models.Model):
    department_name = models.CharField(max_length=100)
    department_description = models.TextField()
    department_created_on = models.DateTimeField(auto_now_add=True)
    department_created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='department_created_by')
    department_updated_on = models.DateTimeField(auto_now=True)
    department_updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='department_updated_by')

    class Meta:
        verbose_name_plural = 'Departments'
        verbose_name = 'Department'

    def __str__(self):
        return self.department_name

class Team(models.Model):
    team_name = models.CharField(max_length=100)
    team_description = models.TextField()
    team_department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='team_department')
    team_created_on = models.DateTimeField(auto_now_add=True)
    team_created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_created_by')
    team_updated_on = models.DateTimeField(auto_now=True)
    team_updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_updated_by')

    class Meta:
        verbose_name_plural = 'Teams'
        verbose_name = 'Team'

    def __str__(self):
        return self.team_name
    
class ChecklistTemplate(models.Model):
    checklist_template_name = models.CharField(max_length=100)
    checklist_template_description = models.TextField()
    checklist_template_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='checklist_template_team')
    checklist_template_created_on = models.DateTimeField(auto_now_add=True)
    checklist_template_created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='checklist_template_created_by')
    checklist_template_updated_on = models.DateTimeField(auto_now=True)
    checklist_template_updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='checklist_template_updated_by')

    class Meta:
        verbose_name_plural = 'Checklist Templates'
        verbose_name = 'Checklist Template'

    def __str__(self):
        return self.checklist_template_name
    
class TaskTemplate(models.Model):
    task_template_name = models.CharField(max_length=100)
    task_template_description = models.TextField()
    task_template_checklist_template = models.ForeignKey(ChecklistTemplate, on_delete=models.CASCADE, related_name='task_template_checklist_template')
    task_template_due_at = models.TimeField()
    task_template_created_on = models.DateTimeField(auto_now_add=True)
    task_template_created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_template_created_by')
    task_template_updated_on = models.DateTimeField(auto_now=True)
    task_template_updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_template_updated_by')

    class Meta:
        verbose_name_plural = 'Task Templates'
        verbose_name = 'Task Template'

    def __str__(self):
        return self.task_template_name
    

class ChecklistInstance(models.Model):
    checklist_instance_checklist_template = models.ForeignKey(ChecklistTemplate, on_delete=models.CASCADE, related_name='checklist_instance_checklist_template')
    checklist_instance_created_on = models.DateTimeField(auto_now_add=True)
    checklist_instance_created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='checklist_instance_created_by')

    class Meta:
        verbose_name_plural = 'Checklist Instances'
        verbose_name = 'Checklist Instance'

    def __str__(self):
        return self.checklist_instance_checklist_template.checklist_template_name
    

class TaskInstance(models.Model):

    STATUS = (
        ('Not Started', 'Not Started'),
        ('Awaiting Verification', 'Awaiting Verification'),
        ('Completed', 'Completed'),
    )

    task_instance_task_template = models.ForeignKey(TaskTemplate, on_delete=models.CASCADE, related_name='task_instance_task_template')
    task_instance_processed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_instance_processed_by')
    task_instance_processed_on = models.DateTimeField(auto_now=True)
    task_instance_processor_notes = models.TextField()
    task_instance_verified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_instance_verified_by')
    task_instance_verified_on = models.DateTimeField(auto_now=True)
    task_instance_verifier_notes = models.TextField()
    task_instance_status = models.CharField(max_length=100, choices=STATUS, default='Not Started')

    class Meta:
        verbose_name_plural = 'Task Instances'
        verbose_name = 'Task Instance'

    def __str__(self):
        return self.task_instance_task_template.task_template_name

