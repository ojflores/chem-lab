from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from rest_framework_csv import renderers

from api import models
from api.authentication import TokenAuthentication
from api.permissions import IsInstructor


class AssignmentRenderer(renderers.CSVRenderer):
    """
    Customized renderer for assignment CSVs.
    """
    def render(self, data, media_type=None, renderer_context={}, writer_opts=None):
        if data and 'student' in data[0].keys():
            self.header = sorted(data[0].keys())
            self.header.insert(0, self.header.pop(self.header.index('student')))
        return super().render(data, media_type, renderer_context, writer_opts)


class AssignmentCSVView(APIView):
    """
    The GET view for generating a CSV formatted version of an assignment.
    """
    renderer_classes = (AssignmentRenderer,) + tuple(api_settings.DEFAULT_RENDERER_CLASSES)
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsInstructor,)

    def get(self, request, *args, **kwargs):
        """
        Generate a CSV version of an assignment.
        """
        # get assignment from URI
        try:
            assignment = models.Assignment.objects.get(id=kwargs['pk'])
        except models.Assignment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # retrieve all assignment entries and build the CSV
        assignment_entries = models.AssignmentEntry.objects.filter(assignment=assignment).all()
        assignment_csv = []
        for entry in assignment_entries:
            task_entries = models.TaskEntry.objects.filter(assignment_entry=entry).all()
            row = {
                'student': entry.student.wwuid
            }
            # build all columns for the student
            for task in task_entries:
                row[task.task_template.name] = task.raw_input
            assignment_csv.append(row)
        # build the response
        response = Response(assignment_csv)
        # dynamically create file name in response
        response['Content-Disposition'] = 'attachment; filename="{}-{}-{}.csv"'.\
            format(assignment.assignment_template.name,
                   assignment.labgroup.group_name,
                   assignment.labgroup.term)
        return response
