from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import DjangoModelPermissions

from api import serializers
from api.models import Assignment, Instructor, LabGroup, Student
from api.permissions import IsStudentOrInstructor


class AssignmentLCView(ListCreateAPIView):
    """
    The list create view for assignment.
    """
    lookup_field = 'pk'
    serializer_class = serializers.AssignmentSerializer
    permission_classes = (DjangoModelPermissions, IsStudentOrInstructor)

    def get_queryset(self):
        # get student'l labgroup's assignments
        if self.request.user.groups.filter(name='Student').exists():
            return Assignment.objects.filter(labgroup=Student.objects.get(user=self.request.user).labgroup)
        # get all assignments for every labgroup instructor owns
        else:
            instructor = Instructor.objects.get(user=self.request.user)
            labgroups = LabGroup.objects.filter(instructor=instructor).all()
            return Assignment.objects.filter(labgroup__in=labgroups)

    def list(self, request, *args, **kwargs):
        response = super(AssignmentLCView, self).list(request, *args, **kwargs)
        response.data = {
            'assignments': response.data,
        }
        return response


class AssignmentRUDView(RetrieveUpdateDestroyAPIView):
    """
    The retrieve update destroy view for assignment.
    """
    lookup_field = 'pk'
    serializer_class = serializers.AssignmentSerializer
    permission_classes = (DjangoModelPermissions, IsStudentOrInstructor)

    def get_queryset(self):
        return Assignment.objects.all()

