from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from admin_panel.users.serializers.auth import CustomAuthTokenSerializer


class CustomAuthTokenView(ObtainAuthToken):
    """
    API endpoint for user authentication and token generation
    """
    serializer_class = CustomAuthTokenSerializer

    @swagger_auto_schema(
        tags=['Authentication'],
        operation_summary="Obtain auth token",
        operation_description="Authenticate user and get token along with user details",
        request_body=CustomAuthTokenSerializer,
        responses={
            200: openapi.Response(
                description="Successful authentication",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'token': openapi.Schema(type=openapi.TYPE_STRING),
                        'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'organization': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
                        'email': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            ),
            400: "Invalid credentials"
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = CustomAuthTokenSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = User.objects.filter(email=email).first()
        token, created = Token.objects.get_or_create(user=user)
        organization = None
        if user and user.employee:
            organization = user.employee.organization_id
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'organization': organization,
            'email': user.email
        })