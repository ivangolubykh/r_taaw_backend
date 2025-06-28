from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from users.validators.user_settings import UserSettingValidator

from .models import UserSetting

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    nickname = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ("username", "password", "email", "nickname")

    @staticmethod
    def validate_password(value):
        validate_password(value)
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)
        return user


class CurrentUserSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "nickname",
            "display_name",
            "email",
            "language",
            "avatar",
        )


class UserSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSetting
        fields = ["key", "value", "last_modified"]
        read_only_fields = ["last_modified"]

    def validate(self, data):
        key = data.get("key")
        value = data.get("value")
        data["value"] = UserSettingValidator.validate(key, value)
        return data
