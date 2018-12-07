from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import DjangoModelPermissions
from api import serializers
from api.models import TaskEntry
from api.authentication import TokenAuthentication


class TaskEntryLCView(ListCreateAPIView):
    """
    The list create view for task entry
    """
    authentication_classes = (SessionAuthentication,)
    permission_classes = (DjangoModelPermissions,)
    lookup_field = 'pk'
    serializer_class = serializers.TaskEntrySerializer
    def get_queryset(self):
        return TaskEntry.objects.all()

    def list(self, request, *args, **kwargs):
        response = super(TaskEntryLCView, self).list(request, *args, **kwargs)
        response.data = {
            'task_entry': response.data,
        }
        return response

class TaskEntryRUDView(RetrieveUpdateDestroyAPIView):
    """
    The retrieve update destroy view for task entry.
    """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permissions_classes = (DjangoModelPermissions,)
    lookup_field = 'pk'
    serializer_class = serializers.TaskEntrySerializer

    def get_queryset(self):
        return TaskEntry.objects.all()