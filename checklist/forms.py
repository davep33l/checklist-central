from django import forms
from .models import Department


class CustomDepartmentEditForm(forms.ModelForm):
    
        class Meta:
            model = Department
            fields = ['name', 'description']
            widgets = {
                'description': forms.Textarea(attrs={'rows': 2}),
            }


class CustomDepartmentCreateForm(forms.ModelForm):
        
            class Meta:
                model = Department
                fields = ['name', 'description']
                widgets = {
                    'description': forms.Textarea(attrs={'rows': 2}),
                }


