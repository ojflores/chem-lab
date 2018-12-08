from django.conf import settings
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from datetime import datetime
from pytz import timezone

from api import serializers
from api.permissions import IsStudent
from api.models import AssignmentEntry, Assignment, Student
from api.serializers import AssignmentEntrySerializer


class AssignmentEntryView(RetrieveAPIView):
    """
    The retrieve view for assignment entries.
    """
    permission_classes = (IsAuthenticated, IsStudent)
    lookup_field = 'assignment'
    serializer_class = AssignmentEntrySerializer

    def get_queryset(self):
        student = Student.objects.get(user=self.request.user)
        return AssignmentEntry.objects.filter(student=student, assignment=self.kwargs['assignment']).all()


class AssignmentEntryStartView(APIView):
    """
    The create view for assignment entries.
    """
    permission_classes = (IsAuthenticated, IsStudent)

    def post(self, request, *args, **kwargs):
        student = Student.objects.get(user=request.user)
        # check if assignment exists and get it
        try:
            assignment = Assignment.objects.get(id=kwargs['assignment'])
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
        # check if assignment exists
        try:
            assignment = Assignment.objects.get(id=kwargs['assignment'])
        except Assignment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # get student
        student = Student.objects.get(user=request.user)
        # check if assignment has been started
        try:
            assignment_entry = AssignmentEntry.objects.get(assignment=assignment, student=student)
        except AssignmentEntry.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # set the submit date
        assignment_entry.submit_date = datetime.now(timezone(settings.TIME_ZONE))
        assignment_entry.save()
        # response
        serialized_assignment_entry = serializers.AssignmentEntrySerializer(assignment_entry)
        return Response(serialized_assignment_entry.data, status=status.HTTP_200_OK)
