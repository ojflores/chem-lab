from django.contrib.auth.models import ContentType, Group, Permission
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.status import HTTP_201_CREATED

from api import models, serializers
from api.models import Student


class StudentLCView(ListCreateAPIView):
    """
    The list create view for students.
    """
    authentication_classes = (SessionAuthentication,)
    permission_classes = (DjangoModelPermissions,)
    lookup_field = 'wwuid'
    serializer_class = serializers.StudentSerializer

    def get_queryset(self):
        return Student.objects.all()

    def list(self, request, *args, **kwargs):
        response = super(StudentLCView, self).list(request, *args, **kwargs)
        response.data = {
            'students': response.data,
        }
        return response

    def create(self, request, *args, **kwargs):
        response = super(StudentLCView, self).create(request, *args, **kwargs)
        # create the student group if it does not exist
        group, created = Group.objects.get_or_create(name='Student')
        # do not modify permissions if the request fails
        if response.status_code is not HTTP_201_CREATED:
            return response
        if created:
            # get permissions for all student models
            content_types = [
                ContentType.objects.get_for_model(models.AssignmentEntry),
                ContentType.objects.get_for_model(models.TaskEntry),
            ]
            for ct in content_types:
                group.permissions.add(Permission.objects.filter(content_type=ct).first())
        # add new student to the student group
        group.user_set.add(request.data['user'])
        return response


class StudentRUDView(RetrieveUpdateDestroyAPIView):
    """
    The retrieve update destroy view for students.
    """
    authentication_classes = (SessionAuthentication,)
    permissions_classes = (DjangoModelPermissions,)
    lookup_field = 'pk'
    serializer_class = serializers.StudentSerializer

    def get_queryset(self):
        return Student.objects.all()
