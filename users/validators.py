from rest_framework import serializers

from localization.language_consts import LANGUAGE_CODE_MAP

from .models import UserSettingKey


def validate_locale(value: str):
    normalized = value.lower().replace("_", "-")
    if normalized not in LANGUAGE_CODE_MAP.values():
        raise serializers.ValidationError(f"Invalid locale: {value}")


def validate_theme_mode(value: str):
    if value not in ("light", "dark", "system"):
        raise serializers.ValidationError(f"Invalid theme mode: {value}")


VALIDATORS_BY_KEY = {
    UserSettingKey.LOCALE: validate_locale,
    UserSettingKey.THEME_MODE: validate_theme_mode,
    # UserSettingKey.SORT_MODE: validate_sort_mode — in the future
}
