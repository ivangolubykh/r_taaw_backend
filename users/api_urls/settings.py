from django.urls import path

from users.views import UserSettingView

urlpatterns = [
    path("", UserSettingView.as_view(), name="user-settings"),
]
