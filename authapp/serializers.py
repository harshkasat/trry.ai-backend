from rest_framework import serializers

class GoogleSocialAuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    email_verified = serializers.BooleanField()
    name = serializers.CharField()
    picture = serializers.URLField()
    given_name = serializers.CharField()

    # validate the email_verified field
    def validate_email_verified(self, value):
        if value:
            return value
        raise serializers.ValidationError("Email not verified")
    


class AuthSerializer(serializers.Serializer):
    code = serializers.CharField(required=False)
    error = serializers.CharField(required=False)