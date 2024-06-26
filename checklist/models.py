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
