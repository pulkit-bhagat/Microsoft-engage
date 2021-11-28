from django.contrib import admin
from . import models

admin.site.register(models.Teacher)
admin.site.register(models.Course)
admin.site.register(models.Student)
admin.site.register(models.Update)
admin.site.register(models.Assignment)
admin.site.register(models.AssignmentSolution)