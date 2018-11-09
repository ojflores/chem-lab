from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Student, LabGroup


class EnrollView(APIView):
    """
    The POST view for enrolling in a LabGroup.
    """
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        """
        Enroll in a lab group.
        """
        # load the lab group from the database
        lab_group = LabGroup.objects.get(pk=request.data['lab_group'])
        if request.data['enroll_key'] == lab_group.enroll_key:
            Student.objects.filter(user=request.user).update(lab_group=lab_group)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)