from django.contrib.auth.models import ContentType, Group, Permission

from api import models


def get_or_create_instructor_permissions():
    # create the instructor group if it does not exist
    group, created = Group.objects.get_or_create(name='Instructor')
    if created:
        # get permissions for all instructor models
        content_types = [
            ContentType.objects.get_for_model(models.Course),
            ContentType.objects.get_for_model(models.LabGroup),
            ContentType.objects.get_for_model(models.Student),
            ContentType.objects.get_for_model(models.Assignment),
            ContentType.objects.get_for_model(models.Assignment),
            ContentType.objects.get_for_model(models.AssignmentTemplate),
            ContentType.objects.get_for_model(models.TaskTemplate)
        ]
        for ct in content_types:
            permissions = Permission.objects.filter(content_type=ct).all()
            for p in permissions:
                group.permissions.add(p)
    return group


def get_or_create_student_permissions():
    # create the student group if it does not exist
    group, created = Group.objects.get_or_create(name='Student')
    if created:
        # add group permissions for all student models
        content_types = [
            ContentType.objects.get_for_model(models.AssignmentEntry),
            ContentType.objects.get_for_model(models.TaskEntry),
        ]
        for ct in content_types:
            permissions = Permission.objects.filter(content_type=ct).all()
            for p in permissions:
                group.permissions.add(p)
    return group
