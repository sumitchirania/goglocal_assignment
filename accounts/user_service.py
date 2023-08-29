import logging

from .models import User

from django.contrib.auth.hashers import check_password, make_password
from rest_framework_simplejwt.tokens import RefreshToken

logger = logging.getLogger(__name__)

class UserService:

    @classmethod
    def authenticate(cls, username, password):

        try:
            user = User.objects.get(username=username)
            if check_password(password, user.password):
                return user
        except User.DoesNotExist:
            return None
        except Exception as e:
            logger.error(e, exc_info=True)
            return None

    @classmethod
    def get_tokens_for_user(cls, user):
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    @classmethod
    def get_all_users(cls):
        return User.objects.all()

