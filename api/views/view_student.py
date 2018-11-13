from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import DjangoModelPermissions


from api import serializers
from api.models import Student


class StudentLCView(ListCreateAPIView):
    """
    The list create view for students.
    """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (DjangoModelPermissions,)
    lookup_field = 'wwuid'
    serializer_class = serializers.StudentSerializer

    def get_queryset(self):
        return Student.objects.all()

    def list(self, request, *args, **kwargs):
        response = super(StudentLCView, self).list(request, *args, **kwargs)
        response.data = {
            'students': response.data,
        }
        return response


class StudentRUDView(RetrieveUpdateDestroyAPIView):
    """
    The retrieve update destroy view for students.
    """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permissions_classes = (DjangoModelPermissions,)
    lookup_field = 'pk'
    serializer_class = serializers.StudentSerializer

    def get_queryset(self):
        return Student.objects.all()
