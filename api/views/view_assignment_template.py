from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import DjangoModelPermissions

from api import serializers
from api.models import AssignmentTemplate
from api.permissions import IsStudentOrInstructor


class AssignmentTemplateLCView(ListCreateAPIView):
    """
    The list create view for AssignmentTemplates.
    """
    lookup_field = 'pk'
    serializer_class = serializers.AssignmentTemplateSerializer
    permission_classes = (DjangoModelPermissions, IsStudentOrInstructor)

    def get_queryset(self):
        return AssignmentTemplate.objects.all()

    # returns a list of AssignmentTemplates
    def list(self, request, *args, **kwargs):
        response = super(AssignmentTemplateLCView, self).list(request, *args, **kwargs)
        response.data = {
            'templates': response.data,
        }
        return response


class AssignmentTemplateRUDView(RetrieveUpdateDestroyAPIView):
    """
    The retrieve update destroy view for AssignmentTemplate.
    """
    lookup_field = 'pk'
    serializer_class = serializers.AssignmentTemplateSerializer
    permission_classes = (DjangoModelPermissions, IsStudentOrInstructor)

    def get_queryset(self):
        return AssignmentTemplate.objects.all()
