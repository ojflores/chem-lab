from django.contrib.auth.models import ContentType, Group, Permission
from rest_framework.permissions import BasePermission, DjangoModelPermissions

from api import models

import copy


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


class ViewDjangoModelPermissions(DjangoModelPermissions):
    """
    Overrides DjangoModelPermissions to enforce view_* permissions.
    """
    def __init__(self):
        self.perms_map = copy.deepcopy(self.perms_map)
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']


class IsInstructor(BasePermission):
    """
    Permission class to determine if the user is an instructor.
    """
    def has_permission(self, request, view):
            return models.Instructor.objects.filter(user=request.user).exists()
