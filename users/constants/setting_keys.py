from django.db import models


class UserSettingKey(models.TextChoices):
    LANGUAGE = "language", "Language"
    THEME_MODE = "theme_mode", "Theme Mode"
    SORT_MODE = "sort_mode", "Sort Mode"
