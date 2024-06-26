from django.contrib import admin
from .models import Department, Team, ChecklistTemplate, TaskTemplate

# Register your models here.

admin.site.register(Department)
admin.site.register(Team)
admin.site.register(ChecklistTemplate)
admin.site.register(TaskTemplate)

