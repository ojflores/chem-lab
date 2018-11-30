from rest_framework import serializers

from api.models import Assignment, AssignmentTemplate


class AssignmentSerializer(serializers.ModelSerializer):
    """
    The serializer for assignment.
    """
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.assignment_template.name

    class Meta:
        model = Assignment
        fields = (
            'pk',
            'assignment_template',
            'name',
            'labgroup',
            'open_date',
            'close_date',
        )

