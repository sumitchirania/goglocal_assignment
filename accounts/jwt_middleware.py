
from django.contrib.auth import get_user_model

from django.utils.deprecation import MiddlewareMixin

from rest_framework_simplejwt.authentication import JWTAuthentication


JWT_authenticator = JWTAuthentication()


class JWTMiddleware(MiddlewareMixin):

    @classmethod
    def process_request(cls, request):
        response = JWT_authenticator.authenticate(request)
        if response is not None:
            # unpacking
            user, token = response
            request.user = get_user_model().objects.get(
                username=token.payload['username'],
                id=token.payload['user_id']
            )


