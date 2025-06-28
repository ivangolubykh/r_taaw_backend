from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from users.constants.setting_keys import UserSettingKey


class UserSettingValidator:
    @staticmethod
    def validate_language(value: str) -> str:
        normalized_value = value.lower().replace("_", "-")
        if normalized_value not in (code for code, label in settings.LANGUAGES):
            raise ValidationError({"value": _(f"Invalid language: '{value}'")})
        return normalized_value

    @staticmethod
    def validate_theme_mode(value: str):
        if value not in {"system", "light", "dark"}:
            raise ValidationError({"value": _(f"Invalid theme mode: '{value}'")})
        return value

    @staticmethod
    def validate_sort_mode(value: str):
        # TODO: Add validation logic for sort_mode when implemented in the frontend
        return value

    @classmethod
    def validate(cls, key: str, value: str) -> str:
        if key not in UserSettingKey.values:
            raise ValidationError({"key": _(f"Unsupported user setting key: '{key}'")})

        method_name = f"validate_{key}"
        validator = getattr(cls, method_name, None)
        if validator is None:
            raise NotImplementedError(f"Validator method '{method_name}' is missing for key '{key}'")
        return validator(value)
