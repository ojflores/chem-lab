from rest_framework import serializers

from api.models import AssignmentEntry


class AssignmentEntrySerializer(serializers.ModelSerializer):
    """
    The serializer for assignment entry.
    """
    submit_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = AssignmentEntry
        fields = (
            'pk',
            'student',
            'assignment',
            'start_date',
            'submit_date',
        )


