from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField()
    email = serializers.RegexField(r'^[^@]+@wallawalla\.edu$', allow_blank=False)

    class Meta:
        model = User
        fields = ('username',
                  'password',
                  'email',
                  'first_name',
                  'last_name',)
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        user = User(**data)
        errors = {}
        # validate email
        if User.objects.filter(email=data.get('email')).exists():
            errors['email'] = 'email is already in use'
        # validate password
        try:
            validate_password(password=data.get('password'), user=user)
        except ValidationError as e:
            errors['password'] = list(e.messages)
        if errors:
            raise serializers.ValidationError(errors)
        return super(UserSerializer, self).validate(data)

    def create(self, validated_data):
        validated_data['username'] = validated_data['email'].split('@')[0]
        return User.objects.create_user(**validated_data)
