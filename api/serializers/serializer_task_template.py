from rest_framework import serializers, status


from api.models import AssignmentTemplate, TaskTemplate


class TaskTemplateSerializer(serializers.ModelSerializer):
    """
    The serializer for Template Tasks.
    """

    def validate_assignment_template(self, value):
        try:
            AssignmentTemplate.objects.get(id=value)
        except AssignmentTemplate.DoesNotExist:
            raise serializers.ValidationError({'detail': 'Not found.'}, code=status.HTTP_404_NOT_FOUND)
        return value

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
        read_only_fields = ('assignment_template',)
