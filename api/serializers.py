from rest_framework import serializers

from api.models import Course
from api.models import AssignmentTemplate

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

class AssignmentTemplateSerializer(serializer.ModelSerializer):
    """
    The serializer for Assignment Templates
    Code By John Dodd
    """
    class Meta:
        model = AssignmentTemplate
        fields = (
            'pk',
            'name',
            'course'
        )