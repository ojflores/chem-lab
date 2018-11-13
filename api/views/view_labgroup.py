from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import DjangoModelPermissions

from api import serializers
from api.models import LabGroup


class LabGroupLCView(ListCreateAPIView):
    """
    The list create view for labgroups.
    """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
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
    The retrieve update destroy view for labgroups.
    """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permissions_classes = (DjangoModelPermissions,)
    lookup_field = 'pk'
    serializer_class = serializers.LabGroupSerializer

    def get_queryset(self):
        return LabGroup.objects.all()
