from rest_framework import serializers

from api.models import LabGroup


class LabGroupFullSerializer(serializers.ModelSerializer):
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


class LabGroupPartialSerializer(serializers.ModelSerializer):
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
        )
