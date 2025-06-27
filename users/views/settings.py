from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import (
    permissions,
    status,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import UserSetting
from ..serializers import UserSettingSerializer


class UserSettingView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(responses=UserSettingSerializer(many=True))
    def get(self, request):
        user = request.user
        settings = UserSetting.objects.filter(user=user)
        serializer = UserSettingSerializer(settings, many=True)
        return Response(serializer.data)

    @extend_schema(request=UserSettingSerializer, responses=UserSettingSerializer)
    def post(self, request):
        user = request.user
        data = request.data.copy()
        key = data.get("key")
        if not key:
            return Response({"detail": "Missing key."}, status=status.HTTP_400_BAD_REQUEST)

        instance = UserSetting.objects.filter(user=user, key=key).first()

        if instance:
            # Check for relevance
            client_timestamp = data.get("last_modified")
            if client_timestamp:
                try:
                    client_dt = timezone.datetime.fromisoformat(client_timestamp)
                    if timezone.is_naive(client_dt):
                        client_dt = timezone.make_aware(client_dt)
                except ValueError:
                    return Response({"detail": "Invalid last_modified timestamp."}, status=status.HTTP_400_BAD_REQUEST)

                # If the server version is newer, we do not update
                if instance.last_modified > client_dt:
                    serializer = UserSettingSerializer(instance)
                    return Response(serializer.data)

        # Update or create
        serializer = UserSettingSerializer(instance, data=data)
        if serializer.is_valid():
            setting = serializer.save(user=user)
            return Response(UserSettingSerializer(setting).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
