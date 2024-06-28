from django.shortcuts import render
from django.views import generic
from .models import Department, Team, ChecklistTemplate, TaskTemplate, ChecklistInstance, TaskInstance, Profile
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.contrib import messages
from .forms import CustomDepartmentEditForm, CustomDepartmentCreateForm


# Create your views here.

def index(request):

    if not request.user.is_authenticated:
        return render(request, 'checklist/index.html')

    if request.user.is_superuser:
        task_instances = TaskInstance.objects.all()
        context = {'task_instances': task_instances,}
        return render(request, 'checklist/index.html', context)
    
    if not Profile.objects.filter(user=request.user).exists():
        return render(request, 'checklist/index.html')

    profile = Profile.objects.get(user=request.user)
    departments = profile.departments.all()

    task_instances = TaskInstance.objects.filter(task_template__checklist_template__team__department__in=departments)
    context = {'task_instances': task_instances,}
    return render(request, 'checklist/index.html', context)


class DepartmentList(generic.ListView):
    model = Department
    context_object_name = 'departments'
    template_name = 'checklist/department_list.html'


class DepartmentEdit(SuccessMessageMixin, UpdateView):
    model = Department
    form_class = CustomDepartmentEditForm
    template_name = 'checklist/department_edit.html'
    context_object_name = 'department'
    success_url = reverse_lazy('departments')
    success_message = "Department updated successfully"


class DepartmentDelete(SuccessMessageMixin, DeleteView):
    model = Department
    template_name = 'checklist/department_confirm_delete.html'
    success_url = reverse_lazy('departments')
    success_message = "Department deleted successfully"


class DepartmentCreate(SuccessMessageMixin, CreateView):
    model = Department
    form_class = CustomDepartmentCreateForm
    template_name = 'checklist/department_edit.html'
    success_url = reverse_lazy('departments')
    success_message = "Department created successfully"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class TeamList(generic.ListView):
    model = Team
    template_name = 'checklist/team_list.html'
    context_object_name = 'teams'
    ordering = ['-name']


class TeamEdit(SuccessMessageMixin, UpdateView):
    model = Team
    fields = ['name', 'department']
    template_name = 'checklist/team_edit.html'
    success_url = reverse_lazy('teams')
    success_message = "Team updated successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = Department.objects.all()
        return context
    
    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class TeamDelete(SuccessMessageMixin, DeleteView):
    model = Team
    template_name = 'checklist/team_confirm_delete.html'
    success_url = reverse_lazy('teams')
    success_message = "Team deleted successfully"


class TeamCreate(SuccessMessageMixin, CreateView):
    model = Team
    fields = ['name', 'department']
    template_name = 'checklist/team_edit.html'
    success_url = reverse_lazy('teams')
    success_message = "Team created successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = Department.objects.all()
        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class ChecklistTemplateList(generic.ListView):
    model = ChecklistTemplate
    template_name = 'checklist/checklist_template_list.html'
    context_object_name = 'checklist_templates'


class ChecklistTemplateEdit(SuccessMessageMixin, UpdateView):
    model = ChecklistTemplate
    fields = ['name', 'team']
    template_name = 'checklist/checklist_template_edit.html'
    success_url = reverse_lazy('checklist_templates')
    success_message = "Checklist updated successfully"
    context_object_name = 'checklist_template'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teams'] = Team.objects.all()
        return context
    
    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class ChecklistTemplateCreate(SuccessMessageMixin, CreateView):
    model = ChecklistTemplate
    fields = ['name', 'team']
    template_name = 'checklist/checklist_template_edit.html'
    success_url = reverse_lazy('checklist_templates')
    success_message = "Checklist created successfully"
    context_object_name = 'checklist_template'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teams'] = Team.objects.all()
        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)
    
    
class ChecklistTemplateDelete(SuccessMessageMixin, DeleteView):
    model = ChecklistTemplate
    template_name = 'checklist/checklist_template_confirm_delete.html'
    success_url = reverse_lazy('checklist_templates')
    success_message = "Checklist deleted successfully"
    context_object_name = 'checklist_template'

class TaskTemplateList(generic.ListView):
    model = TaskTemplate
    template_name = 'checklist/task_template_list.html'
    context_object_name = 'task_templates'

class TaskTemplateEdit(SuccessMessageMixin, UpdateView):
    model = TaskTemplate
    fields = ['name', 'description', 'due_at', 'checklist_template']
    template_name = 'checklist/task_template_edit.html'
    success_url = reverse_lazy('task_templates')
    success_message = "Task updated successfully"
    context_object_name = 'task_template'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['checklist_templates'] = ChecklistTemplate.objects.all()
        return context
    
    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)
    

class TaskTemplateCreate(SuccessMessageMixin, CreateView):
    model = TaskTemplate
    fields = ['name', 'checklist_template', 'description', 'due_at']
    template_name = 'checklist/task_template_edit.html'
    success_url = reverse_lazy('task_templates')
    success_message = "Task created successfully"
    context_object_name = 'task_template'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['checklist_templates'] = ChecklistTemplate.objects.all()
        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)
    

class TaskTemplateDelete(SuccessMessageMixin, DeleteView):
    model = TaskTemplate
    template_name = 'checklist/task_template_confirm_delete.html'
    success_url = reverse_lazy('task_templates')
    success_message = "Task deleted successfully"
    context_object_name = 'task_template'


def initialise_checklists(request):

    checklist_templates = ChecklistTemplate.objects.all()

    if request.method == 'POST':
        checklist = ChecklistTemplate.objects.get(pk=request.POST['checklist_template'])
        new_instance = ChecklistInstance(checklist_template=checklist, created_by=request.user)
        new_instance.save()

        tasks = TaskTemplate.objects.filter(checklist_template=checklist)
        for task in tasks:
            print(task)
            new_task_instance = TaskInstance(task_template=task, checklist_instance=new_instance)
            new_task_instance.save()
            
        messages.success(request, 'Checklist initialised successfully.')
        return redirect('index')
    return render(request, 'checklist/initialise_checklists.html', context={'checklist_templates': checklist_templates})




class ChecklistInstanceList(generic.ListView):
    model = ChecklistInstance
    template_name = 'checklist/checklist_instance_list.html'


class TaskInstanceList(generic.ListView):
    model = TaskInstance
    template_name = 'checklist/task_instance_list.html'

