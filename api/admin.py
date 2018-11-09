from django.contrib import admin

from api import models

admin.site.register(models.Course)
admin.site.register(models.Instructor)
admin.site.register(models.LabGroup)
admin.site.register(models.Student)
admin.site.register(models.Assignment)
admin.site.register(models.AssignmentTemplate)
admin.site.register(models.TaskTemplate)
admin.site.register(models.AssignmentEntry)
admin.site.register(models.TaskEntry)

