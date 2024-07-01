from django.contrib import admin
from .models import (Department, Team, ChecklistTemplate,
                     TaskTemplate, ChecklistInstance, TaskInstance, Profile)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'description',
                    'created_on',
                    'created_by',
                    'updated_on',
                    'updated_by')
    list_filter = ['created_on', 'created_by', 'updated_on', 'updated_by']
    search_fields = ['name', 'description']


admin.site.register(Team)
admin.site.register(ChecklistTemplate)
admin.site.register(TaskTemplate)
admin.site.register(ChecklistInstance)
admin.site.register(TaskInstance)
admin.site.register(Profile)
