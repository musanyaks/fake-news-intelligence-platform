"""Text normalization utilities."""
import re
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
        text = re.sub(r"[""]", '"', text)
        text = re.sub(r"['']", "'", text)
        return text

    @staticmethod
    def normalize_dashes(text: str) -> str:
        return re.sub(r"[–—−]", "-", text)

    @staticmethod
    def normalize(text: str) -> str:
        text = TextNormalizer.normalize_unicode(text)
        text = TextNormalizer.normalize_quotes(text)
        text = TextNormalizer.normalize_dashes(text)
        text = TextNormalizer.normalize_whitespace(text)
        return text.strip()
