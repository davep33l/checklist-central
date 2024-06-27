from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('departments/', views.DepartmentList.as_view(), name='departments'),
    path('departments/<int:pk>/', views.DepartmentEdit.as_view(), name='department_edit'),
    path('departments/<int:pk>/delete/', views.DepartmentDelete.as_view(), name='department_delete'),
    path('departments/new/', views.DepartmentCreate.as_view(), name='department_new'),

    path('teams/', views.TeamList.as_view(), name='teams'),
    path('teams/<int:pk>/', views.TeamEdit.as_view(), name='team_edit'),
    path('teams/<int:pk>/delete/', views.TeamDelete.as_view(), name='team_delete'),
    path('teams/new/', views.TeamCreate.as_view(), name='team_new'),

    path('checklist_templates/', views.ChecklistTemplateList.as_view(), name='checklist_templates'),
    path('checklist_templates/<int:pk>/', views.ChecklistTemplateEdit.as_view(), name='checklist_template_edit'),
    path('checklist_templates/<int:pk>/delete/', views.ChecklistTemplateDelete.as_view(), name='checklist_template_delete'),
    path('checklist_templates/new/', views.ChecklistTemplateCreate.as_view(), name='checklist_template_new'),
    
    path('task_templates/', views.TaskTemplateList.as_view(), name='task_templates'),
    path('checklist_instances/', views.ChecklistInstanceList.as_view(), name='checklist_instances'),
    path('task_instances/', views.TaskInstanceList.as_view(), name='task_instances'),
]