from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from api import serializers
from api.models import LabGroup, Instructor

from datetime import date


class LabGroupLCView(ListCreateAPIView):
    """
    The list create view for labgroups.
    """
    lookup_field = 'pk'

    def get_serializer_class(self):
        # only return the enroll_key if the user is an instructor
        if self.request.user.groups.filter(name='Instructor').exists():
            return serializers.LabGroupFullSerializer
        return serializers.LabGroupPartialSerializer

    def get_queryset(self):
        # only return labgroups that belong to the querying instructor
        if self.request.user.groups.filter(name='Instructor').exists():
            instructor = Instructor.objects.get(user = self.request.user.id)
            return LabGroup.objects.filter(term=get_current_term(), instructor=instructor.id)
        return LabGroup.objects.filter(term=get_current_term())

    def list(self, request, *args, **kwargs):
            response = super(LabGroupLCView, self).list(request, *args, **kwargs)
            response.data = {
                'labgroups': response.data,
            }
            return response


class LabGroupRUDView(RetrieveUpdateDestroyAPIView):
    """
    The retrieve update destroy view for labgroups.
    """
    lookup_field = 'pk'

    def get_serializer_class(self):
        if self.request.user.groups.filter(name='Instructor').exists():
            return serializers.LabGroupFullSerializer
        return serializers.LabGroupPartialSerializer

    def get_queryset(self):
        return LabGroup.objects.all()


def get_current_term():
    """
    Returns the current term based on the current date.
    """
    today = date.today()
    # winter term
    if 1 <= today.month < 3 or today.month is 3 and today.day <= 25:
        term = 'WINTER'
    # spring term
    elif 3 <= today.month < 6 or today.month is 6 and today.day <= 16:
        term = 'SPRING'
    # summer term
    elif 6 <= today.month <= 9:
        term = 'SUMMER'
    # fall term
    else:
        term = 'FALL'
    # add year to term
    term += str(today.year)
    return term
