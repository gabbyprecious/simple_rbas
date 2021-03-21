from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.middleware.csrf import CsrfViewMiddleware
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings
from django.urls import reverse
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model

from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from jose import JWTError, jwt

User = get_user_model()

ENCRYPTION_ALGORITHM = "HS256"


def generate_jwt_token(data, min_to_expire=None):
    """
    Generates and returns account token with expiration of min_to_expire minutes
    :param data:
    :param min_to_expire:
    Returns:
    """
    payload = data.copy()

    if min_to_expire is None:
        min_to_expire = 15
    expire = datetime.utcnow() + timedelta(minutes=min_to_expire)
    payload.update({"exp": expire})
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=ENCRYPTION_ALGORITHM)
    return token


def decrypt_jwt_token(token):
    """
    Decrypts authentication token and returns content
    :param token:
    :return:
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY)
    except JWTError:
        payload = None
    return payload


class CSRFCheck(CsrfViewMiddleware):
    def _reject(self, request, reason):
        """
        We are returning the failure reason instead of an HttpResponse
        :param request:
        :param reason:
        :return:
        """
        return reason


class SafeJWTAuthentication(BaseAuthentication):
    """
    Custom Authentication Class that authenticates users from cookies (http-only)
    instead of from Authorization key in headers
    """

    def authenticate(self, request):
        """
        Is required to be implemented (from BaseAuthentication)
        :param request:
        :return:
        """
        authorization_cookie = request.COOKIES.get("Authorization") or request.headers.get("Authorization")

        if not authorization_cookie:
            return None
        try:
            access_token = authorization_cookie.split(" ")[1]
            payload = decrypt_jwt_token(access_token)

        except JWTError:
            return None

        if not payload:
            return None

        user = User.objects.filter(id=payload["user_id"]).first()

        if user is None:
            raise exceptions.AuthenticationFailed("User not found")

        if not user.is_active:
            raise exceptions.AuthenticationFailed("User is inactive")

        self.enforce_csrf(request)
        return user, None

    def enforce_csrf(self, request):
        """
        Enforces CSRF Validation
        :param request:
        :return:
        """
        return
