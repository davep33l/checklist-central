from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import Department, Team, ChecklistTemplate, TaskTemplate, ChecklistInstance, TaskInstance

# Create your views here.

def index(request):
    # render the index.html page
    return render(request, 'checklist/index.html')


class DepartmentList(generic.ListView):
    model = Department
    template_name = 'checklist/department_list.html'


class TeamList(generic.ListView):
    model = Team
    template_name = 'checklist/team_list.html'


class ChecklistTemplateList(generic.ListView):
    model = ChecklistTemplate
    template_name = 'checklist/checklist_template_list.html'


class TaskTemplateList(generic.ListView):
    model = TaskTemplate
    template_name = 'checklist/task_template_list.html'


class ChecklistInstanceList(generic.ListView):
    model = ChecklistInstance
    template_name = 'checklist/checklist_instance_list.html'


class TaskInstanceList(generic.ListView):
    model = TaskInstance
    template_name = 'checklist/task_instance_list.html'

