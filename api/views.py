from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from api import serializers
from api.models import Course


class CourseLCView(ListCreateAPIView):
    '''
    The list create view for courses.
    '''
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
    '''
    The retrieve update destroy view for courses.
    '''
    lookup_field = 'pk'
    serializer_class = serializers.CourseSerializer

    def get_queryset(self):
        return Course.objects.all()

