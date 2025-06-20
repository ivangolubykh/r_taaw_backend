from django.utils import translation
from django.utils.deprecation import MiddlewareMixin

from localization.language_consts import LANGUAGE_CODE_MAP


class NormalizingLocaleMiddleware(MiddlewareMixin):
    """
    Middleware that normalizes the language code from HTTP headers
    to match the format used in settings.LANGUAGES (e.g., zh-CN → zh-Hans).
    """

    def process_request(self, request):
        # Get the language from the request headers
        lang = translation.get_language_from_request(request, check_path=True)

        # Normalize the code to match Django's expected format
        normalized = LANGUAGE_CODE_MAP.get(lang.lower(), lang)

        # Activate the normalized language
        translation.activate(normalized)
        request.LANGUAGE_CODE = normalized
