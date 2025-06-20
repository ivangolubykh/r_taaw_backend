from django.urls import (
    include,
    path,
)

urlpatterns = [
    path("auth/", include("users.api_urls.auth")),
    path("me/", include("users.api_urls.me")),
    path("settings/", include("users.api_urls.settings")),
]
