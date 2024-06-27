from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('departments/', views.DepartmentList.as_view(), name='departments'),
    path('teams/', views.TeamList.as_view(), name='teams'),
    path('checklist_templates/', views.ChecklistTemplateList.as_view(), name='checklist_templates'),
    path('task_templates/', views.TaskTemplateList.as_view(), name='task_templates'),
    path('checklist_instances/', views.ChecklistInstanceList.as_view(), name='checklist_instances'),
    path('task_instances/', views.TaskInstanceList.as_view(), name='task_instances'),
]