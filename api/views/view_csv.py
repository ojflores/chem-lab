from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView

from rest_framework_csv import renderers

from api.authentication import TokenAuthentication
from api.permissions import IsInstructor
from api import models


class AssignmentRenderer(renderers.CSVRenderer):
    def render(self, data, media_type=None, renderer_context={}, writer_opts=None):
        if data:
            self.header = sorted(data[0].keys())
            self.header.insert(0, self.header.pop(self.header.index('student')))
        return super().render(data, media_type, renderer_context, writer_opts)


class AssignmentCSVView(APIView):
    """
    The GET view for generating a CSV formatted version of an assignment.
    """
    renderer_classes = (AssignmentRenderer,)
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    # TODO: fix the instructor permission class
    # permission_classes = (IsInstructor,)

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
                'student': entry.student.id
            }
            # build all columns for the student
            for task in task_entries:
                row[task.task_template.name] = task.raw_input
            assignment_csv.append(row)
        # return the CSV
        return Response(assignment_csv)
