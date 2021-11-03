from .utils import allowed_file, save_video,ALLOWED_EXTENSIONS
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from .serializers import LoginSerializer
from django.contrib.auth import login as django_login, logout as django_logout
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser




class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        django_login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=200)

class LogoutView(APIView):

    def post(self, request):
        django_logout(request)
        return Response(status=204)


class UploadVideo(APIView):
    parser_classes = (FormParser, MultiPartParser)
    permission_classes = (IsAuthenticated,)
    
    def post(self,request):
        if 'file' not in request.data:
            return Response('No file part' , status.HTTP_400_BAD_REQUEST)
        file = request.FILES.get('file',None)
        if file.name == '':
            return Response('No file attached or filename is blank' , status.HTTP_404_NOT_FOUND)
        if file and allowed_file(file.name):
            return save_video(file)
        else:
            return Response('Allowed file types are: ' + ', '.join(ALLOWED_EXTENSIONS) , status.HTTP_400_BAD_REQUEST)