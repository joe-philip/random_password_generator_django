from random import choice, shuffle

from django.http.response import FileResponse
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from root.utils.utils import success

from .models import Profile
from .serializers import ProfileSerializer

# Create your views here.


class ContactUsAPI(APIView):
    def post(self, request: Request) -> Response:
        from .serializers import ContactUsSerializer

        serializer = ContactUsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer.send_email()
        return Response(success(serializer.data))


class RandomPasswordAPI(APIView):
    def post(self, request: Request) -> Response:
        from .serializers import RandomPasswordSerializer
        serializer = RandomPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        SYMBOLS = tuple(range(33, 48))
        DIGITS = tuple(range(48, 58))
        UPPPER_CASE = tuple(range(65, 91))
        LOWER_CASE = tuple(range(97, 123))
        password = ''
        while len(password) < serializer.validated_data.get('password_length'):
            if serializer.validated_data.get('upper_case'):
                password += chr(choice(UPPPER_CASE))
            if serializer.validated_data.get('lower_case'):
                password += chr(choice(LOWER_CASE))
            if serializer.validated_data.get('numeric'):
                password += chr(choice(DIGITS))
            if serializer.validated_data.get('symbols'):
                password += chr(choice(SYMBOLS))
        password = password[:serializer.validated_data.get('password-length')]
        password_list = list(password)
        shuffle(password_list)
        return Response(success(''.join(password_list)))


class ProfileAPI(APIView):
    def get(self, request: Request) -> Response:
        profile = Profile.objects.first()
        serializer = ProfileSerializer(profile, context={'request': request})
        return Response(success(serializer.data))


class DownloadResumeAPI(APIView):
    def get(self, request, id: int) -> FileResponse:
        if (profile := Profile.objects.filter(id=id)).exists():
            return FileResponse(profile.first().resume, as_attachment=True, filename='resume.pdf')
        raise NotFound('Profile not found')
