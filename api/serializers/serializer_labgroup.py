from rest_framework import serializers

from api.models import LabGroup


class LabGroupFullSerializer(serializers.ModelSerializer):
    """
    The full serializer for labgroups. Includes the enroll key.
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
    The partial serializer for labgroups. Excludes the enroll key.
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
