from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse

def index(request):
    return HttpResponse("Pong!")

class Ping(APIView):
    """
    Ping sample endpoint.
    """
    @staticmethod
    def get(request):
        return Response({'result': 'pong!'})
