from django.contrib import auth
from django.utils.timezone import now
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from .services import create_user


class AuthHelper:

    @staticmethod
    def login(data, user):
        if user:
            user.last_login = now()
            user.save()
            token, _ = Token.objects.get_or_create(user=user)
            token.delete()
            token = Token.objects.create(user=user)
            data['token'] = token.key
            data['type'] = user.type
        return data

    @staticmethod
    def logout(user):
        try:
            token = Token.objects.get(user=user)
            token.delete()
        except Token.DoesNotExist:
            pass


class Logout(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        AuthHelper.logout(self.request.user)
        return Response()


class SignIn(APIView):
    serializer_class = serializers.LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.data
            user = auth.authenticate(email=data['email'].lower(), password=request.data['password'])
            response = AuthHelper.login(data, user)
            return Response(data=response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignUp(APIView):
    serializer_class = serializers.SignUp
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = create_user(**serializer.validated_data)
            data = serializer.data
            response = AuthHelper.login(data, user)
            return Response(data=response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePassword(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer = serializers.PasswordUser

    def put(self, request, *args, **kwargs):
        data = self.serializer(request.user, data=request.data)
        if data.is_valid(raise_exception=True):
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
