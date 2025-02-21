# services.py
from django.conf import settings
from django.shortcuts import redirect
from django.core.exceptions import ValidationError
from urllib.parse import urlencode
from typing import Dict, Any
from django.contrib.auth import get_user_model
import requests
from rest_framework_simplejwt.tokens import RefreshToken
import logging
from authapp.serializers import GoogleSocialAuthSerializer

logger = logging.getLogger(__name__)

GOOGLE_ACCESS_TOKEN_OBTAIN_URL = 'https://oauth2.googleapis.com/token'
GOOGLE_USER_INFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'
LOGIN_URL = f'{settings.BASE_API_URL}/internal/login'

User = get_user_model()

# Exchange authorization token with access token
def google_get_access_token(code: str, redirect_uri: str) -> str:
    logger.info('Exchanging authorization code for access token.')
    data = {
        'code': code,
        'client_id': settings.GOOGLE_CLIENT_ID,
        'client_secret': settings.GOOGLE_CLIENT_SECRET,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }

    response = requests.post(GOOGLE_ACCESS_TOKEN_OBTAIN_URL, data=data)
    if not response.ok:
        logger.error('Failed to obtain access token from Google. Response: %s', response.content)
        raise ValidationError('Could not get access token from Google.')
    
    access_token = response.json()['access_token']
    logger.info('Access token obtained successfully.')

    return access_token

# Get user info from google
def google_get_user_info(access_token: str) -> Dict[str, Any]:
    logger.info('Fetching user info from Google.')
    response = requests.get(
        GOOGLE_USER_INFO_URL,
        params={'access_token': access_token}
    )

    
    userinfo_serializer = GoogleSocialAuthSerializer(data=response.json())
    userinfo_serializer.is_valid(raise_exception=True)

    validated_data = userinfo_serializer.validated_data
    if 'error' in validated_data:
        logger.error('Failed to obtain user info from Google.')
        raise ValidationError('Could not get user info from Google.')
    
    
    logger.info('User info obtained successfully.')
    return validated_data


def get_user_data(validated_data):
    logger.info('Processing user data.')
    redirect_uri = settings.GOOGLE_REDIRECT_URI  # Use the redirect URI from settings

    code = validated_data.get('code')
    error = validated_data.get('error')

    if error or not code:
        logger.error('Error or missing authorization code.')
        params = urlencode({'error': error})
        return redirect(f'{LOGIN_URL}?{params}')
    
    access_token = google_get_access_token(code=code, redirect_uri=redirect_uri)
    user_data = google_get_user_info(access_token=access_token)
    split_name = user_data.get('name').split(' ')
    if user_data is not None:
        logger.info('User data obtained successfully')
        print('Email', user_data.get('email'))
        print('First Name', user_data.get('given_name'))
        split_name = user_data.get('name').split(' ')
        print('Last Name', split_name[-1])
        print('Picture', user_data['picture'])
        user, created = User.objects.get_or_create(
            email=user_data['email'],
            defaults={
                'first_name': user_data.get('given_name'),
                'last_name': split_name[-1],
                'profile_picture': user_data['picture']
            }
        )
    else:
        logger.error('Failed to obtain user data from Google.')
        raise ValidationError('Could not get user data from Google.')

    # Create jwt refresh and access tokens
    token = RefreshToken.for_user(user)
    profile_data = {
        'email': user_data['email'],
        'first_name': user_data.get('given_name'),
        'last_name': split_name[-1],
        'profile_picture': user_data['picture'],
        'refresh_token': str(token),
        'access_token': str(token.access_token)
    }
    logger.info('User data processed successfully.')
    return profile_data