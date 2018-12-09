from django.conf import settings
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import DjangoModelPermissions

from datetime import datetime
from pytz import timezone

from api import serializers
from api.models import AssignmentTemplate, Assignment, Student
from api.permissions import IsStudentOrInstructor


class AssignmentTemplateLCView(ListCreateAPIView):
    """
    The list create view for AssignmentTemplates.
    """
    lookup_field = 'pk'
    serializer_class = serializers.AssignmentTemplateSerializer
    permission_classes = (DjangoModelPermissions, IsStudentOrInstructor)

    def get_queryset(self):
        if self.request.user.groups.filter(name='Student').exists():
            # get student
            student = Student.objects.get(user=self.request.user)
            # get all assignments open to the user
            current_time = datetime.now(timezone(settings.TIME_ZONE))
            assignments = Assignment.objects.filter(labgroup=student.labgroup,
                                                    open_date__lt=current_time,
                                                    close_date__gt=current_time).all()
            # get "open" assignment templates from the students course
            return AssignmentTemplate.objects.filter(
                assignment__in=assignments, course=student.labgroup.course).all()
        return AssignmentTemplate.objects.all()

    # returns a list of AssignmentTemplates
    def list(self, request, *args, **kwargs):
        response = super(AssignmentTemplateLCView, self).list(request, *args, **kwargs)
        response.data = {
            'templates': response.data,
        }
        return response


class AssignmentTemplateRUDView(RetrieveUpdateDestroyAPIView):
    """
    The retrieve update destroy view for AssignmentTemplate.
    """
    lookup_field = 'pk'
    serializer_class = serializers.AssignmentTemplateSerializer
    permission_classes = (DjangoModelPermissions, IsStudentOrInstructor)

    def get_queryset(self):
        return AssignmentTemplate.objects.all()
