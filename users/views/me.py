from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import CurrentUserSerializer


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CurrentUserSerializer

    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)
