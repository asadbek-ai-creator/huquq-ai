"""
Language utilities for huquqAI system
Til qollaniw ushın kómeқlik funktsialar
"""

from typing import Dict, Optional
from src.core.config import get_config


class LanguageUtils:
    """Language utility class"""

    def __init__(self):
        self.config = get_config()
        self.terminology = self.config.terminology.get("karakalpak", {})
        self.translations = self.config.terminology.get("translations", {})

    def translate_term(self, term: str, from_lang: str = "kaa",
                       to_lang: str = "en") -> str:
        """Translate legal term between languages"""
        # Find term in Karakalpak terminology
        term_key = None
        for key, value in self.terminology.items():
            if value.lower() == term.lower():
                term_key = key
                break

        if not term_key:
            return term  # Return original if not found

        # Get translation
        term_translations = self.translations.get(term_key, {})
        return term_translations.get(to_lang, term)

    def get_supported_languages(self) -> list:
        """Get list of supported languages"""
        return self.config.language.supported

    def is_supported_language(self, lang_code: str) -> bool:
        """Check if language is supported"""
        return lang_code in self.config.language.supported

    def get_default_language(self) -> str:
        """Get default language"""
        return self.config.language.default

    def get_term_translations(self, term_key: str) -> Dict[str, str]:
        """Get all translations for a term"""
        translations = self.translations.get(term_key, {})
        result = {"kaa": self.terminology.get(term_key, "")}
        result.update(translations)
        return result

    def detect_language(self, text: str) -> Optional[str]:
        """
        Detect language of text
        Simple detection based on terminology
        In production, use proper language detection library
        """
        # Check for Karakalpak specific characters
        karakalpak_chars = set("ǵńıúó")
        if any(char in text for char in karakalpak_chars):
            return "kaa"

        # Check for specific terms
        for term in self.terminology.values():
            if term.lower() in text.lower():
                return "kaa"

        return None


def get_language_utils() -> LanguageUtils:
    """Get language utils instance"""
    return LanguageUtils()
