from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Student, LabGroup
from api import permissions
from api.serializers import StudentSerializer, EnrollStatusSerializer


class EnrollView(APIView):
    """
    The POST view for enrolling in a LabGroup.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        Retrieve the enrollment status of the current user.
        """
        # get the student if they exist
        try:
            student = Student.objects.get(user=request.user.id)
        except Student.DoesNotExist:
            student = None
        # compile the data to be serialized
        data = {
            'user': request.user,
            'student': student,
        }
        # serialize and return the response
        serializer = EnrollStatusSerializer(data)
        return Response(serializer.data)

    def post(self, request):
        """
        Enroll in a labgroup.
        """
        # ensure all parameters are present in the request data
        for param in ('wwuid', 'labgroup', 'enroll_key'):
            if param not in request.data.keys():
                return Response(status=status.HTTP_400_BAD_REQUEST)
        # load the labgroup from the database
        try:
            labgroup = LabGroup.objects.get(id=request.data['labgroup'])
        except LabGroup.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # check enroll key
        if request.data['enroll_key'] != labgroup.enroll_key:
            return Response(status=status.HTTP_403_FORBIDDEN)
        # delete student if it exists
        try:
            student = Student.objects.get(user=request.user)
            student.delete()
        except Student.DoesNotExist:
            pass
        # validate student data in request
        student_data = {
            'user': request.user.id,
            'labgroup': labgroup.id,
            'wwuid': request.data['wwuid'],
        }
        serializer = StudentSerializer(data=student_data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # create the student
        student = Student(user=request.user, labgroup=labgroup, wwuid=request.data['wwuid'])
        student.save()
        # add new student to the student group
        group = permissions.get_or_create_student_permissions()
        group.user_set.add(request.user)
        # return successful response
        return Response(status=status.HTTP_204_NO_CONTENT)
