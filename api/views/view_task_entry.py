from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import DjangoModelPermissions

from api import serializers
from api.models import TaskEntry, Assignment, AssignmentEntry
from api.permissions import IsStudent


class TaskEntryLCView(ListCreateAPIView):
    """
    The list create view for task entry
    """
    permission_classes = (DjangoModelPermissions, IsStudent)
    serializer_class = serializers.TaskEntrySerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return TaskEntry.objects.filter(assignment_entry=AssignmentEntry.objects.get(assignment=self.kwargs['assignment']))

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
    permissions_classes = (DjangoModelPermissions, IsStudent)
    serializer_class = serializers.TaskEntrySerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return TaskEntry.objects.all()
