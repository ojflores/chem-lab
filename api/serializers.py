from rest_framework import serializers

from api.models import Course, Student, LabGroup, Instructor


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
    M.Davis and J.Berglund
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
    Temp serializer for Lab_group.
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

class InstructorSerializer(serializers.ModelSerializer):
    """
    Temp serializer for Instructor.
    """
    class Meta:
        model = Instructor
        fields = (
            'pk',
            'user',
            'wwuid',
        )