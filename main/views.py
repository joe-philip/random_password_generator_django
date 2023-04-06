from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.


class ContactUsAPI(APIView):
    def post(self, request: Request) -> Response:
        from root.utils.utils import success

        from .serializers import ContactUsSerializer
        
        serializer = ContactUsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(success(serializer.data))
