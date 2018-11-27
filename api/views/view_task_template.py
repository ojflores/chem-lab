from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import DjangoModelPermissions

from api import serializers
from api.authentication import TokenAuthentication
from api.models import TaskTemplate


class TaskTemplateLCView(ListCreateAPIView):
    """
    The list create view for TaskTemplates
    """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (DjangoModelPermissions,)
    lookup_field = 'pk'
    serializer_class = serializers.TaskTemplateSerializer

    # returns all query objects of this type
    def get_queryset(self):
        return TaskTemplate.objects.all()

    # returns a list of TaskTemplates
    def list(self, request, *args, **kwargs):
        response = super(TaskTemplateLCView, self).list(request,*args,**kwargs)
        response.data = {
            'task templates': response.data,
        }
        return response


class AssignmentTemplateRUDView(RetrieveUpdateDestroyAPIView):
    """
    The retrieve update destroy view for TaskTemplates
    """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permissions_classes = (DjangoModelPermissions,)
    lookup_field = 'pk'
    serializer_class = serializers.TaskTemplateSerializer

    def get_queryset(self):
        return TaskTemplate.objects.all()
