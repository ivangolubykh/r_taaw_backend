from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib.auth.password_validation import validate_password
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError(_("Username is required"))
        user = self.model(username=username, **extra_fields)
        if password:
            validate_password(password, user)
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class UserModel(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_("Username"), max_length=150, unique=True)
    email = models.EmailField(_("Email address"), blank=True, null=True)
    nickname = models.CharField(_("Nickname"), max_length=150, blank=True, null=True)

    is_active = models.BooleanField(_("Active"), default=True)
    is_staff = models.BooleanField(_("Staff status"), default=False)
    email_verified_at = models.DateTimeField(_("Email verified at"), null=True, blank=True)

    language = models.CharField(
        _("Preferred language"),
        max_length=10,
        choices=settings.LANGUAGES,
        default=settings.LANGUAGE_CODE,
    )
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)

    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    @property
    def display_name(self):
        return self.nickname or self.username

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.username


class UserSettingKey(models.TextChoices):
    LOCALE = "locale", "Locale"
    THEME_MODE = "theme_mode", "Theme Mode"
    SORT_MODE = "sort_mode", "Sort Mode"


class UserSetting(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    key = models.CharField(max_length=50, choices=UserSettingKey.choices)
    value = models.TextField()
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["user", "key"]

    def __str__(self):
        return f"{self.user.username} - {self.key}"

    def as_dict(self):
        return {
            "key": self.key,
            "value": self.value,
            "last_modified": self.last_modified.isoformat(),
        }
