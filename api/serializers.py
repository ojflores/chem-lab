from rest_framework import serializers

from api.models import Course, Instructor, LabGroup, Student


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
    The serializer for instructors.
    """
    class Meta:
        model = Instructor
        fields = (
            'pk',
            'user',
            'wwuid',
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


class LabGroupSerializer(serializers.ModelSerializer):
    """
    The serializer for lab groups.
    """
    class Meta:
        model = LabGroup
        fields = (
            'pk',
            'course',
            'instructor',
            'term',
            'enroll_key',
        )
