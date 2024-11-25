from rest_framework import serializers


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        return attrs
