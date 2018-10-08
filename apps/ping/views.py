from rest_framework.views import APIView
from rest_framework.response import Response


class Ping(APIView):
    """
    Ping sample endpoint.
    """
    @staticmethod
    def get(request):
        return Response({'result': 'pong!'})
