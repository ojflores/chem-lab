from rest_framework import serializers

from api.models import LabGroup


class LabGroupBaseSerializer(serializers.ModelSerializer):
    """
    The base serializer for labgroups.
    """
    term = serializers.RegexField(regex=r'(WINTER|SPRING|SUMMER|FALL)[0-9]{4}')


class LabGroupFullSerializer(LabGroupBaseSerializer):
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


class LabGroupPartialSerializer(LabGroupBaseSerializer):
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
