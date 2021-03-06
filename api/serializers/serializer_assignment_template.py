from rest_framework import serializers

from api.models import AssignmentTemplate


class AssignmentTemplateSerializer(serializers.ModelSerializer):
    """
    The serializer for assignment templates.
    """
    class Meta:
        model = AssignmentTemplate
        fields = (
            'pk',
            'name',
            'course'
        )

