from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework_simplejwt.tokens import RefreshToken
from authapp.google_auth import get_user_data
from django.shortcuts import redirect
from django.conf import settings
from django.http import HttpRequest
from rest_framework.views import APIView
from .serializers import AuthSerializer




import logging
logger = logging.getLogger(__name__)

class AllowOnlyLocalhost(BasePermission):
    """
    Allows access only to localhost
    """
    def has_permission(self, request:HttpRequest, view):
        allowed_origins = ["http://localhost:3000"]
        allowed_ips = ["127.0.0.1", "localhost"]

        origin = request.META.get("HTTP_ORIGIN")
        remote_addr = request.META.get("REMOTE_ADDR")

        return origin in allowed_origins or remote_addr in allowed_ips

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
    
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({"message": "Server is running Health Check"})


# views that handle 'localhost://8000/auth/api/login/google/'
class GoogleLoginApi(APIView):
    authentication_classes = []
    permission_classes = [AllowOnlyLocalhost]
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

        # Return user data as JSON response
        # response =  Response(user_data)
        response = redirect("http://localhost:3000/dashboard")
        response.set_cookie('access_token', user_data['access_token'], httponly=True, secure=True, samesite='Lax')
        response.set_cookie('refresh_token', user_data['refresh_token'], httponly=True, secure=True, samesite='Lax')
        response.content = user_data
        return response
        