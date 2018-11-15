from rest_framework import serializers

from api.models import AssignmentTemplate


class AssignmentTemplateSerializer(serializers.ModelSerializer):
    """
    The serializer for assignmenttemplate.
    """
    class Meta:
        model = AssignmentTemplate
        fields = (
            'course',
            'name',
        )