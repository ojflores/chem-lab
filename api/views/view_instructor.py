from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.status import HTTP_201_CREATED

from api import permissions, serializers
from api.models import Instructor


class InstructorLCView(ListCreateAPIView):
    """
    The list create view for instructors.
    """
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

    def create(self, request, *args, **kwargs):
        response = super(InstructorLCView, self).create(request, *args, **kwargs)
        # do not modify permissions if the request fails
        if response.status_code is not HTTP_201_CREATED:
            return response
        # add new instructor to the instructor group
        group = permissions.get_or_create_instructor_permissions()
        group.user_set.add(request.data['user'])
        return response


class InstructorRUDView(RetrieveUpdateDestroyAPIView):
    """
    The retrieve update destroy view for instructors.
    """
    lookup_field = 'pk'
    serializer_class = serializers.InstructorSerializer

    def get_queryset(self):
        return Instructor.objects.all()
