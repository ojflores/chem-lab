from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from datetime import datetime
from rest_framework import status

from api import serializers
from api.models import AssignmentEntry, Assignment

class AssignmentEntryStartView(APIView):
    """
    The create view for assingment_entrys.
    """
    authentication_classes = (SessionAuthentication,)
    permission_classes = (DjangoModelPermissions,)
    lookup_field = 'pk'
    serializer_class = serializers.AssignmentEntrySerializer



class AssignmentEntrySubmitView(APIView):
    """
    The submit view for assignment entry.
    """
    authentication_classes = (SessionAuthentication,)
    permissions_classes = (DjangoModelPermissions,)
    lookup_field = 'pk'
    serializer_class = serializers.AssignmentEntrySerializer

    def post(self, request, *args, **kwargs):
        # TODO check assignment exists
        # TODO check assignment entry exists
        # TODO check if assignment has already been submitted

        assignment = Assignment.objects.get(id=kwargs['assignment_pk'])
        assignment_entry = AssignmentEntry.objects.get(assignment=assignment)
        assignment_entry.submit_date = datetime.now()
        assignment_entry.save()

        return Response(status=status.HTTP_200_OK)