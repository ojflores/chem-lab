from rest_framework import serializers

from api.models import Instructor


class InstructorSerializer(serializers.ModelSerializer):
    """
    The serializer for instructors.
    """
    class Meta:
        model = Instructor
        fields = (
            'pk',
            'user',
            'wwuid',
        )
