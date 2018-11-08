from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import DjangoModelPermissions

from api import serializers
from api.models import Course, Student, LabGroup, Instructor


class CourseLCView(ListCreateAPIView):
    """
    The list create view for courses.
    """
    authentication_classes = (SessionAuthentication,)
    permission_classes = (DjangoModelPermissions,)
    lookup_field = 'pk'
    serializer_class = serializers.CourseSerializer

    def get_queryset(self):
        return Course.objects.all()

    def list(self, request, *args, **kwargs):
        response = super(CourseLCView, self).list(request, *args, **kwargs)
        response.data = {
            'courses': response.data,
        }
        return response


class CourseRUDView(RetrieveUpdateDestroyAPIView):
    """
    The retrieve update destroy view for courses.
    """
    authentication_classes = (SessionAuthentication,)
    permissions_classes = (DjangoModelPermissions,)
    lookup_field = 'pk'
    serializer_class = serializers.CourseSerializer

    def get_queryset(self):
        return Course.objects.all()

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


class StudentRUDView(RetrieveUpdateDestroyAPIView):
    """
    The retrieve update destroy view for students.
    """
    authentication_classes = (SessionAuthentication,)
    permissions_classes = (DjangoModelPermissions,)
    lookup_field = 'wwuid'
    serializer_class = serializers.StudentSerializer

    def get_queryset(self):
        #name = Student.user.get_full_name()
        return Student.objects.all() #name


class LabGroupLCView(ListCreateAPIView):
    """
    The list create view for lab_group.
    """
    authentication_classes = (SessionAuthentication,)
    permission_classes = (DjangoModelPermissions,)
    lookup_field = 'pk'
    serializer_class = serializers.LabGroupSerializer

    def get_queryset(self):
        return LabGroup.objects.all()

    def list(self, request, *args, **kwargs):
        response = super(LabGroupLCView, self).list(request, *args, **kwargs)
        response.data = {
            'labgroups': response.data,
        }
        return response


class LabGroupRUDView(RetrieveUpdateDestroyAPIView):
    """
    The retrieve update destroy view for lab_group.
    """
    authentication_classes = (SessionAuthentication,)
    permissions_classes = (DjangoModelPermissions,)
    lookup_field = 'pk'
    serializer_class = serializers.LabGroupSerializer

    def get_queryset(self):
        return LabGroup.objects.all()


class InstructorLCView(ListCreateAPIView):
    """
    The list create view for Instructors.
    """
    authentication_classes = (SessionAuthentication,)
    permission_classes = (DjangoModelPermissions,)
    lookup_field = 'pk'
    serializer_class = serializers.InstructorSerializer

    def get_queryset(self):
        return Instructor.objects.all()

    def list(self, request, *args, **kwargs):
        response = super(InstructorLCView, self).list(request, *args, **kwargs)
        response.data = {
            'instructors': response.data,
        }
        return response


class InstructorRUDView(RetrieveUpdateDestroyAPIView):
    """
    The retrieve update destroy view for Instructors.
    """
    authentication_classes = (SessionAuthentication,)
    permissions_classes = (DjangoModelPermissions,)
    lookup_field = 'pk'
    serializer_class = serializers.InstructorSerializer

    def get_queryset(self):
        return Instructor.objects.all()

