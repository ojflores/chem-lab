from rest_framework import serializers

from api.models import Assignment


class AssignmentSerializer(serializers.ModelSerializer):
    """
    The serializer for assignment.
    """
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.assignment_template.name

    def validate(self, data):
        super_data = super(AssignmentSerializer, self).validate(data)
        # check if they have the same course
        if data['labgroup'].course != data['assignment_template'].course:
            raise serializers.ValidationError('the labgroup and assignment template must be a part of the same course')
        return super_data

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
