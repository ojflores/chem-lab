from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import DjangoModelPermissions
from rest_framework import status

from api import permissions, serializers
from api.models import Student


class StudentLCView(ListCreateAPIView):
    """
    The list create view for students.
    """
    lookup_field = 'wwuid'
    serializer_class = serializers.StudentSerializer
    permission_classes = (DjangoModelPermissions, permissions.IsInstructor)

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
        # do not modify permissions if the request fails
        if response.status_code is not status.HTTP_201_CREATED:
            return response
        # add new student to the student group
        group = permissions.get_or_create_student_permissions()
        group.user_set.add(request.data['user'])
        return response


class StudentRUDView(RetrieveUpdateDestroyAPIView):
    """
    The retrieve update destroy view for students.
    """
    lookup_field = 'pk'
    serializer_class = serializers.StudentSerializer
    permission_classes = (DjangoModelPermissions, permissions.IsInstructor)

    def get_queryset(self):
        return Student.objects.all()
