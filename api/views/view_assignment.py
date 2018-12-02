from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from api import serializers
from api.authentication import TokenAuthentication
from api.models import Assignment


class AssignmentLCView(ListCreateAPIView):
    """
    The list create view for assignment.
    """
    lookup_field = 'pk'
    serializer_class = serializers.AssignmentSerializer

    def get_queryset(self):
        return Assignment.objects.all()

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

    def get_queryset(self):
        return Assignment.objects.all()

