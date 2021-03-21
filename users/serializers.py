import django.contrib.auth.password_validation as validators
from django.contrib.auth import get_user_model
from django.core import exceptions
from rest_framework import serializers

User = get_user_model()

class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    level = serializers.IntegerField(required=False)
    password = serializers.CharField(trim_whitespace=False)

    def validate_email(self, email):
        """
        Raises exception if email already exist
        :return:
        """
        try:
            user = User.objects.get(email=email)
            if user.is_active:
                raise serializers.ValidationError("user with that email already exists")
        except User.DoesNotExist:
            return email

    def create(self, validated_data):
        """
        Create the user at DB level
        :param validated_data:
        :return:
        """
        level = validated_data.get("level")
        email = validated_data.get("email")
        self.validate_email(email)
        if level > 4 or level < 0:
            raise serializers.ValidationError("level does not exist")
        user = User.objects.create_user(**validated_data)
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "level",)