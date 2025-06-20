from django.urls import path

from users.views import MeView

urlpatterns = [
    path("", MeView.as_view(), name="me"),
]
