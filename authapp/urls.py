from django.urls import path
from .views import (
    AuthHealthCheck,
    GoogleLoginApi,
    UserProfileView
)

urlpatterns = [
    path('health/', AuthHealthCheck.as_view(), name='auth-health-check'),
    path('api/login/google/', GoogleLoginApi.as_view(), name='google-login-api'),
    path('api/login/profile/', UserProfileView.as_view(), name='google-login-api'),
]