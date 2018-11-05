from rest_framework import serializers

from api.models import Course
from api.models import LabGroup




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

class LabGroupSerializer(serializers.ModelSerializer):
    """
        The serializer for LabGroups
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