from django.utils import translation
from django.utils.deprecation import MiddlewareMixin

# Mapping for normalizing incoming language codes
# key — a language code possibly sent by the browser
# value — the normalized code as defined in settings.LANGUAGES (compatible with Django)
LANGUAGE_CODE_MAP = {
    # Chinese (Simplified)
    "zh": "zh-hans",
    "zh-cn": "zh-hans",
    "zh-sg": "zh-hans",
    "zh-hans": "zh-hans",
    # Chinese (Traditional)
    "zh-tw": "zh-hant",
    "zh-hk": "zh-hant",
    "zh-mo": "zh-hant",
    "zh-hant": "zh-hant",
    # Portuguese (Brazil)
    "pt-br": "pt-br",
    "pt_br": "pt-br",
    # Portuguese (Portugal)
    "pt": "pt",
    # Norwegian Bokmål
    "no": "nb",
    "nb": "nb",
    # Hebrew
    "iw": "he",  # Legacy code for Hebrew
    # Indonesian
    "in": "id",  # Legacy code for Indonesian
    # Generic normalization (identity mapping for the rest)
    "sq": "sq",
    "ar": "ar",
    "az": "az",
    "eu": "eu",
    "bn": "bn",
    "bg": "bg",
    "ca": "ca",
    "hr": "hr",
    "cs": "cs",
    "da": "da",
    "nl": "nl",
    "en": "en",
    "eo": "eo",
    "et": "et",
    "fi": "fi",
    "fr": "fr",
    "gl": "gl",
    "de": "de",
    "el": "el",
    "he": "he",
    "hi": "hi",
    "hu": "hu",
    "is": "is",
    "id": "id",
    "ga": "ga",
    "it": "it",
    "ja": "ja",
    "ko": "ko",
    "lv": "lv",
    "lt": "lt",
    "ms": "ms",
    "fa": "fa",
    "pl": "pl",
    "ro": "ro",
    "ru": "ru",
    "sk": "sk",
    "sl": "sl",
    "es": "es",
    "sv": "sv",
    "tl": "tl",
    "th": "th",
    "tr": "tr",
    "uk": "uk",
    "ur": "ur",
}


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
