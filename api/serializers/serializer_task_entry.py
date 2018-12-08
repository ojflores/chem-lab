from rest_framework import serializers
from api.models import TaskEntry


class TaskEntrySerializer(serializers.ModelSerializer):
    """
    Serializer for Task Entries
    """
    class Meta:
        model = TaskEntry
        fields = (
            'pk',
            'assignment_entry',
            'task_template',
            'attempts',
            'raw_input',
        )
