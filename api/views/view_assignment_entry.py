from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from datetime import datetime
from rest_framework import status

from api import serializers
from api.permissions import IsStudent
from api.models import AssignmentEntry, Assignment, Student


class AssignmentEntryStartView(APIView):
    """
    The create view for assignment entries.
    """
    permission_classes = (IsAuthenticated, IsStudent)

    def post(self, request, *args, **kwargs):
        # TODO: check that student is in assignments labgroup
        student = Student.objects.get(user=request.user)
        # check if assignment exists and get it
        try:
            assignment = Assignment.objects.get(id=kwargs['assignment_pk'])
        except Assignment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # check if student is in the assignments labgroup
        if student.labgroup is None or assignment.labgroup.id is not student.labgroup.id:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # check if student has already started the assignment
        if AssignmentEntry.objects.filter(student=student, assignment=assignment).exists():
            return Response(status=status.HTTP_409_CONFLICT)
        assignment_entry = AssignmentEntry(student=student, assignment=assignment)
        assignment_entry.save()
        # response
        serialized_assignment_entry = serializers.AssignmentEntrySerializer(assignment_entry)
        return Response(serialized_assignment_entry.data, status=status.HTTP_201_CREATED)


class AssignmentEntrySubmitView(APIView):
    """
    The submit view for assignment entries.
    """
    permission_classes = (IsAuthenticated, IsStudent)

    def post(self, request, *args, **kwargs):
        # TODO check assignment exists
        # TODO check assignment entry exists
        # TODO check if assignment has already been submitted

        assignment = Assignment.objects.get(id=kwargs['assignment_pk'])
        student = Student.objects.get(user=request.user)
        assignment_entry = AssignmentEntry.objects.get(assignment=assignment, student=student)
        assignment_entry.submit_date = datetime.now()
        assignment_entry.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
