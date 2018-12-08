from rest_framework import serializers

from api.serializers import StudentSerializer
from register.serializers import UserSerializer


class EnrollStatusSerializer(serializers.Serializer):
    """
    The serializer for enroll status.
    """
    user = UserSerializer(read_only=True)
    student = StudentSerializer(read_only=True)
