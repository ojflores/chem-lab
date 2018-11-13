from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Student, LabGroup


class EnrollView(APIView):
    """
    The POST view for enrolling in a LabGroup.
    """
    authentication_classes = (SessionAuthentication, TokenAuthentication)

    def post(self, request):
        """
        Enroll in a labgroup.
        """
        # load the labgroup from the database
        labgroup = LabGroup.objects.get(pk=request.data['labgroup'])
        if request.data['enroll_key'] == labgroup.enroll_key:
            Student.objects.filter(user=request.user).update(labgroup=labgroup)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)