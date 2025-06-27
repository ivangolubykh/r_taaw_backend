import logging

from django.conf import settings

logger = logging.getLogger("django.request")


class LogAllRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if settings.DEBUG:
            logger.info(f"{request.method} {request.get_full_path()} => {response.status_code}")
        return response
