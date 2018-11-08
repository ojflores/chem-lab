from rest_framework import serializers

from api.models import Course, Student


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


class StudentSerializer(serializers.ModelSerializer):
    """
    The serializer for students.
    """
    class Meta:
        model = Student
        fields = (
            'pk',
            'lab_group',
            'user',
            'wwuid',
        )
