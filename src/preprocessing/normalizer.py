"""Text normalization utilities."""

import unicodedata


class TextNormalizer:
    """Normalize text for consistent processing."""

    @staticmethod
    def normalize_unicode(text: str) -> str:
        return unicodedata.normalize("NFKC", text)

    @staticmethod
    def normalize_whitespace(text: str) -> str:
        return " ".join(text.split())

    @staticmethod
    def normalize_quotes(text: str) -> str:
        text = text.replace(chr(8220), '"').replace(chr(8221), '"')
        text = text.replace(chr(8216), "'").replace(chr(8217), "'")
        return text

    @staticmethod
    def normalize_dashes(text: str) -> str:
        text = text.replace(chr(8211), "-")  # en dash
        text = text.replace(chr(8212), "-")  # em dash
        text = text.replace(chr(8722), "-")  # minus sign
        return text

    @staticmethod
    def normalize(text: str) -> str:
        text = TextNormalizer.normalize_unicode(text)
        text = TextNormalizer.normalize_quotes(text)
        text = TextNormalizer.normalize_dashes(text)
        text = TextNormalizer.normalize_whitespace(text)
        return text.strip()
