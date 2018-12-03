from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from register.serializers import UserSerializer


class RegisterView(CreateAPIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)
    # serializer_class = (UserSerializer,)
    lookup_field = 'pk'

    def get_serializer_class(self):
        return UserSerializer
