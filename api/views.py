from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import DjangoModelPermissions

from api import serializers
from api.models import Course, AssignmentTemplate


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


class AssignmentTemplateLCView(ListCreateAPIView):
    """
    The list create view for AssignmentTemplates.
    -JTD
    """
    authentication_classes = (SessionAuthentication,)
    permission_classes = (DjangoModelPermissions,)
    lookup_field = 'pk'
    serializer_class = serializers.AssignmentTemplateSerializer

    #returns all query objects of this type I think...
    def get_queryset(self):
        return AssignmentTemplate.objects.all()

    #returns a list of AssignmentTemplates
    def List(self, request, *args, **kwargs):
        #create a response object that will be returned
        response = super(AssignmentTemplateLCView,self).list(request,*args,**kwargs)
        #name the response data? so that it can be referenced later by UI maybe??
        response.data = {
            'assignmenttemplates' : response.data,
        }
        #return the response
        return response


