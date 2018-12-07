from rest_framework import serializers

from api.models import LabGroup, Instructor


class LabGroupBaseSerializer(serializers.ModelSerializer):
    """
    The base serializer for labgroups.
    """
    term = serializers.RegexField(regex=r'(WINTER|SPRING|SUMMER|FALL)[0-9]{4}')

    def validate_instructor(self, instructor):
        # check if the requester set himself in the instructor field
        if self.context['request'].user != instructor.user:
            raise serializers.ValidationError('specified instructor is not the instructor making the request')
        return instructor


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
