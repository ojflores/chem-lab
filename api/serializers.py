from rest_framework import serializers

from api.models import Course


class CourseSerializer(serializers.ModelSerializer):
    '''
    The serializer for courses.
    '''
    class Meta:
        model = Course
        fields = (
            'pk',
            'name',
        )

