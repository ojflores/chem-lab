from rest_framework import serializers

from api.models import TaskTemplate


class TaskTemplateSerializer(serializers.ModelSerializer):
    """
    The serializer for Template Tasks.
    """
    class Meta:
        model = TaskTemplate
        fields = (
            'pk',
            'assignment_template',
            'name',
            'summary',
            'prompt',
            'prompt_format',
            'image_urls',
            'attempts_allowed',
            'numeric_accuracy',
            'numeric_only',
        )
