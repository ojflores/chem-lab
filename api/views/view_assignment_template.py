from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import DjangoModelPermissions

from api import serializers
from api.authentication import TokenAuthentication
from api.models import AssignmentTemplate


class AssignmentTemplateLCView(ListCreateAPIView):
    """
    The list create view for AssignmentTemplates.
    """
    permission_classes = (DjangoModelPermissions,)
    lookup_field = 'pk'
    serializer_class = serializers.AssignmentTemplateSerializer

    # returns all query objects of this type I think...
    def get_queryset(self):
        return AssignmentTemplate.objects.all()

    # returns a list of AssignmentTemplates
    def list(self, request, *args, **kwargs):
        response = super(AssignmentTemplateLCView, self).list(request,*args,**kwargs)
        response.data = {
            'templates': response.data,
        }
        return response


class AssignmentTemplateRUDView(RetrieveUpdateDestroyAPIView):
    """
    The retrieve update destroy view for AssignmentTemplate.
    """
    permissions_classes = (DjangoModelPermissions,)
    lookup_field = 'pk'
    serializer_class = serializers.AssignmentTemplateSerializer

    def get_queryset(self):
        return AssignmentTemplate.objects.all()
