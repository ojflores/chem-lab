from rest_framework.views import APIView


class RegisterView(APIView):
    authentication_classes = None

    def post(self, request, *args, **kwargs):
        pass
