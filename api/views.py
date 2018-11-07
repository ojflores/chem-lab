from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.views import APIView

from api import serializers
from api.models import Course, Student
from api.models import LabGroup


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
    this list creates view for LabGroups
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
    The retrieve update destroy view for labgroups
    """
    authentication_classes = (SessionAuthentication,)
    permissions_classes = (DjangoModelPermissions,)
    lookup_field = 'pk'
    serializer_class = serializers.LabGroupSerializer

    def get_queryset(self):
        return LabGroup.objects.all()


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

