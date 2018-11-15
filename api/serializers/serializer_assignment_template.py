from rest_framework import serializers

from api.models import AssignmentTemplate


class AssignmentTemplateSerializer(serializers.ModelSerializer):
    """
    The serializer for Assignment Templates.
    """
    class Meta:
        model = AssignmentTemplate
        fields = (
            'pk',
            'name',
            'course'
        )
