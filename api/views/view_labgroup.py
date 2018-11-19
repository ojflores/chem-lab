from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import DjangoModelPermissions

from api import serializers
from api.authentication import TokenAuthentication
from api.models import Instructor, LabGroup

from datetime import date


class LabGroupLCView(ListCreateAPIView):
    """
    The list create view for labgroups.
    """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (DjangoModelPermissions,)
    lookup_field = 'pk'

    def get_serializer_class(self):
        if self.request.user.groups.filter(name='Instructor').exists():
            return serializers.LabGroupFullSerializer
        return serializers.LabGroupPartialSerializer

    def get_queryset(self):
        return LabGroup.objects.filter(term=currentTerm())

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

    def get_serializer_class(self):
        if self.request.user.groups.filter(name='Instructor').exists():
            return serializers.LabGroupFullSerializer
        return serializers.LabGroupPartialSerializer

    def get_queryset(self):
        return LabGroup.objects.all()


def currentTerm():
    today = date.today()
    # winter term
    if 1 <= today.month < 3 or today.month is 3 and today.day <= 25:
        term = 'WINTER'
    # spring term
    elif 3 <= today.month < 6 or today.month is 6 and today.day <= 16:
        term = 'SPRING'
    # summer term
    elif 6 <= today.month <= 9:
        term = 'SUMMER'
    # fall term
    else:
        term = 'FALL'
    # add year to term
    term += str(today.year)
    return term
