from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import (
    UserModel,
    UserSetting,
    UserSettingKey,
)


class UserSettingsAPITestCase(APITestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(username="testuser", password="testpass123")
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        self.url = reverse("user-settings")

    def test_get_empty_settings(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_create_new_setting(self):
        data = {
            "key": UserSettingKey.LOCALE,
            "value": "en",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["key"], "locale")
        self.assertEqual(response.data["value"], "en")
        self.assertIn("last_modified", response.data)

    def test_update_existing_setting(self):
        UserSetting.objects.create(user=self.user, key=UserSettingKey.LOCALE, value="en")
        data = {
            "key": UserSettingKey.LOCALE,
            "value": "ru",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["value"], "ru")

    def test_invalid_key(self):
        data = {
            "key": "nonexistent_key",
            "value": "value",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_value_for_locale(self):
        data = {
            "key": UserSettingKey.LOCALE,
            "value": "invalid_locale",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_conflict_resolution_old_timestamp(self):
        setting = UserSetting.objects.create(user=self.user, key=UserSettingKey.LOCALE, value="en")

        old_time = timezone.now() - timedelta(days=1)

        data = {
            "key": UserSettingKey.LOCALE,
            "value": "ru",
            "last_modified": old_time.isoformat(),  # ← simulate legacy client
        }

        response = self.client.post(self.url, data)
        setting.refresh_from_db()

        self.assertEqual(setting.value, "en")  # the server should not accept the old value
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["value"], "en")  # the server will return the current value

    def test_conflict_resolution_new_timestamp(self):
        # Set the initial value
        setting = UserSetting.objects.create(
            user=self.user, key=UserSettingKey.LOCALE, value="en", last_modified=timezone.now() - timedelta(days=1)
        )

        # Sending a new value (current time)
        data = {
            "key": UserSettingKey.LOCALE,
            "value": "ru",
        }
        response = self.client.post(self.url, data)
        setting.refresh_from_db()

        # We are waiting for the value to be updated.
        self.assertEqual(setting.value, "ru")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["value"], "ru")
