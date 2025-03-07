from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        print("🔍 CookieJWTAuthentication called")

        # First, try default header authentication
        header_auth = super().authenticate(request)
        if header_auth:
            print("✅ Authenticated via header")
            return header_auth

        # If no header, check cookies
        raw_token = request.COOKIES.get("access_token")
        if not raw_token:
            print("❌ No token found in cookies")
            return None  # No token, return None

        try:
            validated_token = self.get_validated_token(raw_token)
            print("✅ Token validated successfully")
            return self.get_user(validated_token), validated_token
        except AuthenticationFailed:
            print("❌ Invalid token")
            return None
