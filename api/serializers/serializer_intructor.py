from rest_framework import serializers

from api.models import Instructor


class InstructorSerializer(serializers.ModelSerializer):
    """
    The serializer for instructors.
    """
    wwuid = serializers.CharField(write_only=True)

    class Meta:
        model = Instructor
        fields = (
            'pk',
            'user',
            'wwuid',
        )
