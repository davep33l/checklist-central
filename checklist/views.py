from django.shortcuts import render
from django.views import generic
from .models import (
    Department,
    Team,
    ChecklistTemplate,
    TaskTemplate,
    ChecklistInstance,
    TaskInstance,
    Profile,
)
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.contrib import messages
from .forms import CustomDepartmentEditForm, CustomDepartmentCreateForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

# Create your views here.


@login_required
def index(request):

    if not request.user.is_authenticated:
        return render(request, "checklist/index.html")

    if request.user.is_superuser:
        task_instances = TaskInstance.objects.all()
        context = {
            "task_instances": task_instances,
        }
        return render(request, "checklist/index.html", context)

    if not Profile.objects.filter(user=request.user).exists():
        return render(request, "checklist/index.html")

    profile = Profile.objects.get(user=request.user)
    department = profile.department

    task_instances = TaskInstance.objects.filter(
        task_template__checklist_template__team__department=department
    )
    context = {
        "task_instances": task_instances,
    }
    return render(request, "checklist/index.html", context)


@method_decorator(login_required, name="dispatch")
class DepartmentList(generic.ListView):
    model = Department
    context_object_name = "departments"
    template_name = "checklist/department_list.html"


@method_decorator(login_required, name="dispatch")
class DepartmentEdit(SuccessMessageMixin, UpdateView):
    model = Department
    form_class = CustomDepartmentEditForm
    template_name = "checklist/department_edit.html"
    context_object_name = "department"
    success_url = reverse_lazy("departments")
    success_message = "Department updated successfully"


@method_decorator(login_required, name="dispatch")
class DepartmentDelete(SuccessMessageMixin, DeleteView):
    model = Department
    template_name = "checklist/department_confirm_delete.html"
    success_url = reverse_lazy("departments")
    success_message = "Department deleted successfully"


@method_decorator(login_required, name="dispatch")
class DepartmentCreate(SuccessMessageMixin, CreateView):
    model = Department
    form_class = CustomDepartmentCreateForm
    template_name = "checklist/department_edit.html"
    success_url = reverse_lazy("departments")
    success_message = "Department created successfully"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class TeamList(generic.ListView):
    model = Team
    template_name = "checklist/team_list.html"
    context_object_name = "teams"
    ordering = ["department__name", "name"]


@method_decorator(login_required, name="dispatch")
class TeamEdit(SuccessMessageMixin, UpdateView):
    model = Team
    fields = ["name", "department", "description"]
    template_name = "checklist/team_edit.html"
    success_url = reverse_lazy("teams")
    success_message = "Team updated successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["departments"] = Department.objects.all()
        return context

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class TeamDelete(SuccessMessageMixin, DeleteView):
    model = Team
    template_name = "checklist/team_confirm_delete.html"
    success_url = reverse_lazy("teams")
    success_message = "Team deleted successfully"


@method_decorator(login_required, name="dispatch")
class TeamCreate(SuccessMessageMixin, CreateView):
    model = Team
    fields = ["name", "department", "description"]
    template_name = "checklist/team_edit.html"
    success_url = reverse_lazy("teams")
    success_message = "Team created successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["departments"] = Department.objects.all()
        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class ChecklistTemplateList(generic.ListView):
    model = ChecklistTemplate
    template_name = "checklist/checklist_template_list.html"
    context_object_name = "checklist_templates"


@method_decorator(login_required, name="dispatch")
class ChecklistTemplateEdit(SuccessMessageMixin, UpdateView):
    model = ChecklistTemplate
    fields = ["name", "team", "description"]
    template_name = "checklist/checklist_template_edit.html"
    success_url = reverse_lazy("checklist_templates")
    success_message = "Checklist updated successfully"
    context_object_name = "checklist_template"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["teams"] = Team.objects.all()
        return context

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class ChecklistTemplateCreate(SuccessMessageMixin, CreateView):
    model = ChecklistTemplate
    fields = ["name", "team", "description"]
    template_name = "checklist/checklist_template_edit.html"
    success_url = reverse_lazy("checklist_templates")
    success_message = "Checklist created successfully"
    context_object_name = "checklist_template"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["teams"] = Team.objects.all()
        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class ChecklistTemplateDelete(SuccessMessageMixin, DeleteView):
    model = ChecklistTemplate
    template_name = "checklist/checklist_template_confirm_delete.html"
    success_url = reverse_lazy("checklist_templates")
    success_message = "Checklist deleted successfully"
    context_object_name = "checklist_template"


@method_decorator(login_required, name="dispatch")
class TaskTemplateList(generic.ListView):
    model = TaskTemplate
    template_name = "checklist/task_template_list.html"
    context_object_name = "task_templates"


@method_decorator(login_required, name="dispatch")
class TaskTemplateEdit(SuccessMessageMixin, UpdateView):
    model = TaskTemplate
    fields = ["name", "description", "due_at", "checklist_template"]
    template_name = "checklist/task_template_edit.html"
    success_url = reverse_lazy("task_templates")
    success_message = "Task updated successfully"
    context_object_name = "task_template"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["checklist_templates"] = ChecklistTemplate.objects.all()
        return context

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class TaskTemplateCreate(SuccessMessageMixin, CreateView):
    model = TaskTemplate
    fields = ["name", "checklist_template", "description", "due_at"]
    template_name = "checklist/task_template_edit.html"
    success_url = reverse_lazy("task_templates")
    success_message = "Task created successfully"
    context_object_name = "task_template"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["checklist_templates"] = ChecklistTemplate.objects.all()
        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class TaskTemplateDelete(SuccessMessageMixin, DeleteView):
    model = TaskTemplate
    template_name = "checklist/task_template_confirm_delete.html"
    success_url = reverse_lazy("task_templates")
    success_message = "Task deleted successfully"
    context_object_name = "task_template"


@login_required
def initialise_checklists(request):

    checklist_templates = ChecklistTemplate.objects.all()

    if not checklist_templates.exists():
        messages.error(request,
                       "There are no checklist templates to initialise.")
        return redirect("index")

    if request.method == "POST":
        checklist = ChecklistTemplate.objects.get(
            pk=request.POST["checklist_template"])
        new_instance = ChecklistInstance(
            checklist_template=checklist, created_by=request.user
        )
        new_instance.save()

        tasks = TaskTemplate.objects.filter(checklist_template=checklist)
        for task in tasks:
            print(task)
            new_task_instance = TaskInstance(
                task_template=task, checklist_instance=new_instance
            )
            new_task_instance.save()

        messages.success(request, "Checklist initialised successfully.")
        return redirect("index")
    return render(
        request,
        "checklist/initialise_checklists.html",
        context={"checklist_templates": checklist_templates},
    )


@method_decorator(login_required, name="dispatch")
class ChecklistInstanceList(generic.ListView):
    model = ChecklistInstance
    template_name = "checklist/checklist_instance_list.html"
    context_object_name = "checklist_instances"


@method_decorator(login_required, name="dispatch")
class ChecklistInstanceDelete(SuccessMessageMixin, DeleteView):
    model = ChecklistInstance
    template_name = "checklist/checklist_instance_confirm_delete.html"
    success_url = reverse_lazy("checklist_instances")
    success_message = "Checklist deleted successfully"
    context_object_name = "checklist_instance"


@method_decorator(login_required, name="dispatch")
class TaskInstanceList(generic.ListView):
    model = TaskInstance
    template_name = "checklist/task_instance_list.html"
    context_object_name = "task_instances"


@method_decorator(login_required, name="dispatch")
class TaskInstanceDelete(SuccessMessageMixin, DeleteView):
    model = TaskInstance
    template_name = "checklist/task_instance_confirm_delete.html"
    success_url = reverse_lazy("task_instances")
    success_message = "Task deleted successfully"
    context_object_name = "task_instance"


@login_required
def task_instance_edit(request, pk):

    task_instance = get_object_or_404(TaskInstance, pk=pk)

    if request.method == "POST":
        if task_instance.processed_by is None:
            task_instance.processed_by = request.user
            task_instance.processed_on = timezone.now()
            task_instance.status = "Awaiting Verification"
            task_instance.save()
            messages.success(request, "Task processed successfully.")
            return redirect("index")
        if task_instance.verified_by is None:
            if task_instance.processed_by == request.user:
                messages.error(request,
                               "You cannot verify a task you processed.")
                return redirect("index")
            task_instance.verified_by = request.user
            task_instance.verified_on = timezone.now()
            task_instance.status = "Completed"
            task_instance.save()
            messages.success(request, "Task verified successfully.")
            return redirect("index")
    return render(
        request,
        "checklist/task_instance_edit.html",
        context={"task_instance": task_instance},
    )


@method_decorator(login_required, name="dispatch")
class UserList(generic.ListView):
    model = Profile
    template_name = "checklist/user_list.html"
    context_object_name = "profiles"
    ordering = ["user__username"]
    paginate_by = 10

    def get_queryset(self):
        return Profile.objects.all().order_by("user__username")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users"] = Profile.objects.all().order_by("user__username")
        return context


class UserEdit(SuccessMessageMixin, UpdateView):
    model = Profile
    fields = ["department"]
    template_name = "checklist/user_edit.html"
    success_url = reverse_lazy("users")
    success_message = "User updated successfully"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users"] = Profile.objects.all().order_by("user__username")
        context["departments"] = Department.objects.all()
        return context

    def form_valid(self, form):
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class UserDelete(SuccessMessageMixin, DeleteView):
    model = Profile
    template_name = "checklist/user_confirm_delete.html"
    success_url = reverse_lazy("users")
    success_message = "User deleted successfully"
    context_object_name = "profile"


@method_decorator(login_required, name="dispatch")
class UserCreate(SuccessMessageMixin, CreateView):
    model = Profile
    fields = ["user", "department"]
    template_name = "checklist/user_edit.html"
    success_url = reverse_lazy("users")
    success_message = "User created successfully"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users"] = Profile.objects.all().order_by("user__username")
        context["departments"] = Department.objects.all()
        context["builtin_users"] = User.objects.all().order_by("username")
        return context

    def form_valid(self, form):
        return super().form_valid(form)

    def form_valid(self, form):
        form.instance.user = form.cleaned_data["user"]
        return super().form_valid(form)

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)
