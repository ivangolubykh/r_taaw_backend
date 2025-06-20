# 🌍 Translation & Localization Guide

This document describes how internationalization (i18n) and localization (l10n) are handled in the **R‑Taaw** project.  
It covers both the static project interface (e.g., labels, buttons) and dynamic user content (e.g., recipes, ingredients).

---

## 🧱 Technologies Used

- **Django Translation Framework** (`gettext`, `.po/.mo` files)
- **Custom translation models** (e.g., `RecipeTranslation`, `IngredientTranslation`)
- **`.arb` files** (used in frontend — see frontend repo)
- **LibreTranslate API** for automatic translations

---

## 🔤 Static Texts (UI Labels, Errors, etc.)

All static text in the backend is marked for translation using Django’s `gettext` or `gettext_lazy`.  

Localization files are stored in:

```
locale/<language_code>/LC_MESSAGES/django.po
```

### ✅ To extract and compile translatable strings

If you've added new `_()` or `gettext()` strings in the codebase and want to update translation files for all supported languages:

1. **Open a shell in the running Django container**:

```bash
docker compose exec django_app bash
```

2. **Run the script to extract messages and update `.po` files**:

```bash
make translations
```

3. **Compile translations** (you can do this in two ways):

- Either manually in the container:

```bash
python manage.py compilemessages
```

- Or **restart the Docker containers**, since the `django_app_preloader` service runs this automatically:

```bash
docker compose up --build
# or run just the preloader if needed:
docker compose run --rm django_app_preloader
```

> ⚠️ Don’t forget: `.po` files must be compiled to `.mo` for translations to take effect at runtime.

This approach ensures consistent builds both in development and in production environments.

---

## 🗃️ Dynamic Content: Recipes & Ingredients

User-entered content is stored in the **original language** and may have **manual or automatic translations**.

### ✍️ Manual Translations

Models:
- `RecipeTranslation`
- `IngredientTranslation`

Each translation is tied to a specific language using a normalized language code (e.g., "en", "ru", "pt-br").

### 🤖 Automatic Translations

Planned in future versions using:
- **LibreTranslate** (via Docker container)
- Auto-detection and translation into supported languages
- Storing only *missing* translations in the background via Celery tasks (to come)

---

## 🏷️ Tags & Categories

Recipe tags (e.g., `"healthy"`, `"quick"`) are fixed and not stored as translatable database fields.

Instead:
- The canonical tag key (e.g., `"healthy"`) is saved in the DB.
- The translated name and description are stored in code in `cookbook/models.py → PREDEFINED_TAGS`.
- Translations are provided via `gettext_lazy`.

---

## 🌐 Language Settings

Supported languages are defined in `settings.py`:

```python
LANGUAGES = [
    ("en", "English"),
    ("eo", "Esperanto - Esperanto"),
    ("et", "Estonian - Eesti"),
    # Add more as needed
]
```

Default language:

```python
LANGUAGE_CODE = "en"
```

---

## 💡 Tips for Translators

- Prefer *natural*, localized phrasing over literal word-for-word translation.
- Keep technical terms and units (e.g., "g", "tbsp", "low carb") consistent.
- Test translations in context via the admin panel or API.

---

## 📂 Frontend Translations

For frontend (Flutter), see:  
📁 [`r_taaw_frontend/lib/l10n/`](https://github.com/ivangolubykh/r_taaw_frontend/tree/main/lib/l10n)

---

## 🧩 Coming Soon

- Automatic translation syncing between frontend/backend
- Per-user language preference stored in user profile
- Admin interface for managing translations (optional)

---
