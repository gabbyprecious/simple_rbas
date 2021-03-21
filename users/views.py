from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import GenericViewSet

from users.serializers import SignUpSerializer, UserSerializer
from users.permissions import (
    OnlyStaffOwnerUserPermission,
    OnlyAdminOwnerUserPermission,
    OnlyInvestorOwnerUserPermission,
    OnlyOwnerUserPermission
)
from users.backends import generate_jwt_token

User = get_user_model()

class SignUpView(GenericViewSet):

    def create(self, request):
        """
        Create User,
        """

        serializer = SignUpSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({"error": serializer.errors, "success": False}, status=status.HTTP_403_FORBIDDEN)
        user = serializer.save()
        user_serializer = UserSerializer(user)

        return Response(
            {"user": user_serializer.data, "success": True},
            status=status.HTTP_201_CREATED,
        )

class LoginView(GenericViewSet):
    def login(self, request):
        """
        Login User and return authentication token (POST REQUEST)
        :param request:
        :return:
        """

        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if not user:
            return Response({"error": "Invalid Credentials", "success": False}, status=status.HTTP_401_UNAUTHORIZED)

        token = generate_jwt_token({"user_id": user.pk}, min_to_expire=1800)
        content = {
            "success": True,
            "message": "You've successfully logged in",
            "email": user.email,
            "user_level": user.level,
            "token": f"Bearer {token}",
            "user_id": user.id,
        }
        response = Response(data=content, status=status.HTTP_200_OK)
        response.set_cookie(
            "Authorization",
            value=f"Bearer {token}",
            httponly=True,
            max_age=settings.COOKIE_TIME,
            expires=settings.COOKIE_TIME,
            samesite="None",
            secure=settings.COOKIE_SECURE, # Cookie is sent from client only over HTTP when flag turned on
        )
        return response


class AllUser(GenericViewSet):

    def get(self, request):
        message = "Every User can visit this url, even unsigned users"
        
        return Response(
            {"message": message , "success": True},
            status=status.HTTP_200_OK,
        )

class OnlyAuthenticatedUser(GenericViewSet):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = User.objects.get(username=request.user.username)
        user_serializer = UserSerializer(user)
        message = "Every authenticated user have access here"

        return Response(
            {"user": user_serializer.data, "message": message, "success": True},
            status=status.HTTP_200_OK,
        )

class OnlyStaffOwnerUser(GenericViewSet):
    permission_classes = [IsAuthenticated, OnlyStaffOwnerUserPermission]

    def get(self, request):
        user = User.objects.get(username=request.user.username)
        user_serializer = UserSerializer(user)
        message = "You can only see this if you're a staff or owner"

        return Response(
            {"user": user_serializer.data, "message": message, "success": True},
            status=status.HTTP_200_OK,
        )

class OnlyAdminStaffOwnerUser(GenericViewSet):
    permission_classes = [IsAuthenticated, OnlyAdminOwnerUserPermission]

    def get(self, request):
        user = User.objects.get(username=request.user.username)
        user_serializer = UserSerializer(user)
        message = "You can only see this if you're an admin staff or owner"

        return Response(
            {"user": user_serializer.data, "message": message, "success": True},
            status=status.HTTP_200_OK,
        )

class OnlyInvestorAndOwnerUser(GenericViewSet):
    permission_classes = [IsAuthenticated, OnlyInvestorOwnerUserPermission]

    def get(self, request):
        user = User.objects.get(username=request.user.username)
        user_serializer = UserSerializer(user)
        message = "You can only see this if you're an investor or owner"

        return Response(
            {"user": user_serializer.data, "message": message, "success": True},
            status=status.HTTP_200_OK,
        )

class OnlyOwnerUser(GenericViewSet):
    permission_classes = [IsAuthenticated, OnlyOwnerUserPermission]

    def get(self, request):
        user = User.objects.get(username=request.user.username)
        user_serializer = UserSerializer(user)
        message = "You can only see this if you're an owner"


        return Response(
            {"user": user_serializer.data, "message": message, "success": True},
            status=status.HTTP_200_OK,
        )