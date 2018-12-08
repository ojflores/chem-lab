from rest_framework import serializers

from api.models import Student


class StudentSerializer(serializers.ModelSerializer):
    """
    The serializer for students.
    """
    class Meta:
        model = Student
        fields = (
            'pk',
            'labgroup',
            'user',
            'wwuid',
        )
