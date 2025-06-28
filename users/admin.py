from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from users.models import (
    UserModel,
    UserSetting,
)

admin.site.unregister(Group)


@admin.register(UserModel)
class UserAdmin(BaseUserAdmin):
    model = UserModel
    list_display = (
        "id",
        "username",
        "nickname",
        "email",
        "email_verified_at",
        "is_staff",
        "is_superuser",
    )
    list_filter = ("is_staff", "is_superuser")
    search_fields = ("username", "email", "nickname")
    ordering = ("id",)
    readonly_fields = ("email_verified_at", "created_at", "updated_at", "last_login")

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("nickname", "email", "avatar", "email_verified_at")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "created_at", "updated_at")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2", "is_staff", "is_superuser"),
            },
        ),
    )


@admin.register(UserSetting)
class UserSettingAdmin(admin.ModelAdmin):
    list_display = ("user", "key", "value", "last_modified")
    list_filter = ("key",)
    search_fields = ("user__username", "value")
    ordering = ("user__id", "key")
    readonly_fields = ("last_modified",)
