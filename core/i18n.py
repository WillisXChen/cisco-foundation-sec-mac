import os
import gettext
from core.config import BASE_DIR

LOCALES_DIR = os.path.join(BASE_DIR, "locales")

# Cache to store Translation objects
_translations = {}

def get_translation(lang_code: str):
    """Lazy load gettext translation based on language code."""
    if lang_code not in _translations:
        try:
            # Fallback=True ensures that it returns original message ID if translated string is not found
            t = gettext.translation('messages', localedir=LOCALES_DIR, languages=[lang_code])
        except FileNotFoundError:
            # If no mapping exists (e.g. English, or a new language without .mo file), fallback to returning the original string
            t = gettext.NullTranslations()
        _translations[lang_code] = t
    return _translations[lang_code]

def _t(text: str, lang: str = "zh-TW", **kwargs) -> str:
    """
    Main function for formatting and translating text.
    Replaces common 'if is_en else' patterns with a single call.
    """
    # map standard chainlit language code (e.g. zh-TW) to gettext convention (zh_TW)
    lang_code = lang.replace("-", "_") if lang else "en"
    
    trans = get_translation(lang_code)
    translated_text = trans.gettext(text)
    
    if kwargs:
        return translated_text.format(**kwargs)
    return translated_text

LANG_NAMES = {
    "zh-TW": "Traditional Chinese",
    "en": "English",
    "ja": "Japanese",
}

def get_lang_name(lang: str = "zh-TW") -> str:
    """Get language name to put inside LLM system prompts."""
    return LANG_NAMES.get(lang, "English")
