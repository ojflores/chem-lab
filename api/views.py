from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.views import APIView


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


class LabGroupLCView(ListCreateAPIView):
    """
    The list create view for lab groups.
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
                'lab_groups': response.data,
            }
            return response


class LabGroupRUDView(RetrieveUpdateDestroyAPIView):
    """
    The retrieve update destroy view for lab groups.
    """
    authentication_classes = (SessionAuthentication,)
    permissions_classes = (DjangoModelPermissions,)
    lookup_field = 'pk'
    serializer_class = serializers.LabGroupSerializer

    def get_queryset(self):
        return LabGroup.objects.all()


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
    lookup_field = 'pk'
    serializer_class = serializers.StudentSerializer

    def get_queryset(self):
        return Student.objects.all()


class InstructorLCView(ListCreateAPIView):
    """
    The list create view for instructors.
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
    The retrieve update destroy view for instructors.
    """
    authentication_classes = (SessionAuthentication,)
    permissions_classes = (DjangoModelPermissions,)
    lookup_field = 'pk'
    serializer_class = serializers.InstructorSerializer

    def get_queryset(self):
        return Instructor.objects.all()


class EnrollView(APIView):
    """
    The POST view for enrolling in a LabGroup.
    """
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        """
        Enroll in a lab group.
        """
        # load the lab group from the database
        lab_group = LabGroup.objects.get(pk=request.data['lab_group'])
        if request.data['enroll_key'] == lab_group.enroll_key:
            Student.objects.filter(user=request.user).update(lab_group=lab_group)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)
