from django.urls import path
from .views import (
    AuthHealthCheck,
    GoogleLoginApi
)

urlpatterns = [
    path('health/', AuthHealthCheck.as_view(), name='auth-health-check'),
    path('api/login/google/', GoogleLoginApi.as_view(), name='google-login-api'),
]