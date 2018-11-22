from rest_framework import serializers

from api.models import Assignment


class AssignmentSerializer(serializers.ModelSerializer):
    """
    The serializer for assignment.
    """
    class Meta:
        model = Assignment
        fields = (
            'assignment_template',
            'labgroup',
            'open_date',
            'close_date',
        )