from rest_framework import serializers

from api.models import Course, Instructor


class CourseSerializer(serializers.ModelSerializer):
    """
    The serializer for courses.
    """
    class Meta:
        model = Course
        fields = (
            'pk',
            'name',
        )


class InstructorSerializer(serializers.ModelSerializer):
    """
    The serializer for courses.
    """
    class Meta:
        model = Instructor
        fields = (
            'pk',
            'user',
            'wwuid',
        )
