from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from api import serializers
from api.models import AssignmentTemplate, TaskTemplate
from api.permissions import IsStudentOrInstructor


class TaskTemplateLCView(ListCreateAPIView):
    """
    The list create view for TaskTemplates.
    """
    permission_classes = (DjangoModelPermissions, IsStudentOrInstructor)
    lookup_field = 'pk'
    serializer_class = serializers.TaskTemplateSerializer

    # returns all query objects of this type
    def get_queryset(self):
        return TaskTemplate.objects.filter(assignment_template=self.kwargs['assignment_template']).all()

    # returns a list of TaskTemplates
    def list(self, request, *args, **kwargs):
        response = super(TaskTemplateLCView, self).list(request, *args, **kwargs)
        response.data = {
            'task_templates': response.data,
        }
        return response

    def post(self, request, *args, **kwargs):
        try:
            return super(TaskTemplateLCView, self).post(request, *args, **kwargs)
        except ValidationError as e:
            return Response(e.detail, status=e.status_code)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.validate_assignment_template(kwargs['assignment_template'])
        return super(TaskTemplateLCView, self).create(request, *args, **kwargs)

    def perform_create(self, serializer):
        assignment_template = AssignmentTemplate.objects.get(id=self.kwargs['assignment_template'])
        serializer.save(assignment_template=assignment_template)


class TaskTemplateRUDView(RetrieveUpdateDestroyAPIView):
    """
    The retrieve update destroy view for TaskTemplates.
    """
    permissions_classes = (DjangoModelPermissions, IsStudentOrInstructor)
    lookup_field = 'pk'
    serializer_class = serializers.TaskTemplateSerializer

    def get_queryset(self):
        return TaskTemplate.objects.all()
