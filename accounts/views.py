import logging

from rest_framework.views import APIView
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework_simplejwt.authentication import JWTAuthentication

from .user_service  import UserService

from .serializers import CustomTokenObtainPairSerializer, CurrentUserSerializer

JWT_authenticator = JWTAuthentication()

logger = logging.getLogger(__name__)


class LoginView(APIView):
    def get(self, request):
        pass

    def post(self, request):
        try:
            username = request.data.get('username', '')
            password = request.data.get('password', '')
            if not username or not password:
                return Response({'data': '', 'success': False, 'msg': 'Username or Password not provided'},
                                status=status.HTTP_200_OK)

            user = UserService().authenticate(username, password)
            if user:
                refresh = CustomTokenObtainPairSerializer.get_token(user)
                return Response({'data': str(refresh.access_token), 'success': True, 'msg': 'Login Successful'},
                                status=status.HTTP_200_OK)
            else:
                return Response({'data': '', 'success': False, 'msg': 'Invalid Credentials'},
                                status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(e, exc_info=True)
            return Response({'data': '', 'success': False, 'msg': 'Internal Server Error'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MyProfileView(APIView):

    def get(self, request):
        try:
            response = JWT_authenticator.authenticate(request)
            if response is not None:
                # unpacking
                user, token = response
                return Response({'data': {'first_name': user.first_name, 'last_name': user.last_name},
                                 'success': True, 'msg': 'Success!!'}, status=status.HTTP_200_OK)
            else:
                return Response({'data': '', 'success': False, 'msg': 'Token Not Provided or Expired'},
                                status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e, exc_info=True)
            return Response({'data': '', 'success': False, 'msg': 'Internal Server Error'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = (AllowAny,)


class CurrentUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserService().get_all_users()
    serializer_class = CurrentUserSerializer
