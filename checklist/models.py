from django.db import models
from django.utils import timezone

# import user
from django.contrib.auth.models import User


# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='department_created_by')
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='department_updated_by')

    class Meta:
        verbose_name_plural = 'Departments'
        verbose_name = 'Department'

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='team_department')
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_created_by')
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_updated_by')

    class Meta:
        verbose_name_plural = 'Teams'
        verbose_name = 'Team'

    def __str__(self):
        return self.name
    
class ChecklistTemplate(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='checklist_template_team')
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='checklist_template_created_by')
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='checklist_template_updated_by')

    class Meta:
        verbose_name_plural = 'Checklist Templates'
        verbose_name = 'Checklist Template'
        ordering = ['name']

    def __str__(self):
        return self.name
    
class TaskTemplate(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    checklist_template = models.ForeignKey(ChecklistTemplate, on_delete=models.CASCADE, related_name='task_template_checklist_template')
    due_at = models.TimeField()
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_template_created_by')
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_template_updated_by')

    class Meta:
        verbose_name_plural = 'Task Templates'
        verbose_name = 'Task Template'

    def __str__(self):
        return self.name
    

class ChecklistInstance(models.Model):
    checklist_template = models.ForeignKey(ChecklistTemplate, on_delete=models.CASCADE, related_name='checklist_instance_checklist_template')
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='checklist_instance_created_by')

    class Meta:
        verbose_name_plural = 'Checklist Instances'
        verbose_name = 'Checklist Instance'

    def __str__(self):
        return self.checklist_template.name
    

class TaskInstance(models.Model):

    STATUS = (
        ('Not Started', 'Not Started'),
        ('Awaiting Verification', 'Awaiting Verification'),
        ('Completed', 'Completed'),
    )

    task_template = models.ForeignKey(TaskTemplate, on_delete=models.CASCADE, related_name='task_instance_task_template')
    processed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_instance_processed_by', null=True, blank=True)
    processed_on = models.DateTimeField(auto_now=True, null=True, blank=True)
    processor_notes = models.TextField(null=True, blank=True)
    verified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_instance_verified_by', null=True, blank=True)
    verified_on = models.DateTimeField(auto_now=True, null=True, blank=True)
    verifier_notes = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUS, default='Not Started')
    checklist_instance = models.ForeignKey(ChecklistInstance, on_delete=models.CASCADE, related_name='task_instance_checklist_instance', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Task Instances'
        verbose_name = 'Task Instance'

    def __str__(self):
        return self.task_template.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # list of departments user can have access to
    departments = models.ManyToManyField(Department, blank=True)

    class Meta:
        verbose_name_plural = 'Profiles'
        verbose_name = 'Profile'

    def __str__(self):
        return self.user.username