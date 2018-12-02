from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Student, LabGroup


class EnrollView(APIView):
    """
    The POST view for enrolling in a LabGroup.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        Enroll in a labgroup.
        """
        # load the labgroup from the database
        try:
            labgroup = LabGroup.objects.get(pk=request.data['labgroup'])
        except LabGroup.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # check enroll key
        if request.data['enroll_key'] != labgroup.enroll_key:
            return Response(status=status.HTTP_403_FORBIDDEN)
        # get users student object
        try:
            student = Student.objects.get(user=request.user)
            student.labgroup = labgroup
            student.save()
        except Student.DoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN)
        # return successful response
        return Response(status=status.HTTP_204_NO_CONTENT)

