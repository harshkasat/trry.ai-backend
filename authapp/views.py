from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
from authapp.serializers import GoogleSocialAuthSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from authapp.google_auth import get_user_data
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth import login
from rest_framework.views import APIView
from .serializers import AuthSerializer




import logging
logger = logging.getLogger(__name__)


def get_tokens_for_user(user):
    try:
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    except Exception as e:
        logger.error(e)
        return {
            'message': 'Error occurred while generating tokens',
            'error': str(e)
        }

class AuthHealthCheck(APIView):
    def get(self, request):
        return Response({"message": "Server is running Health Check"})


# views that handle 'localhost://8000/auth/api/login/google/'
class GoogleLoginApi(APIView):
    def get(self, request, *args, **kwargs):
        auth_serializer = AuthSerializer(data=request.GET)
        auth_serializer.is_valid(raise_exception=True)
        
        validated_data = auth_serializer.validated_data
        logger.info(validated_data)
        if 'error' in validated_data:
            return HttpResponse('Google login failed')
        user_data = get_user_data(validated_data)
        
        # user = User.objects.get(email=user_data['email'])
        # login(request, user)

        return HttpResponse('User logged in successfully')