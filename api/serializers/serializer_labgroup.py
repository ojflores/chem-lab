from rest_framework import serializers

from api.models import LabGroup


class LabGroupSerializer(serializers.ModelSerializer):
    """
    The serializer for labgroups.
    """
    class Meta:
        model = LabGroup
        fields = (
            'pk',
            'course',
            'instructor',
            'group_name',
            'term',
            'enroll_key',
        )
