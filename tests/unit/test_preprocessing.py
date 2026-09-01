"""Unit tests for preprocessing."""
from src.preprocessing.cleaner import TextCleaner
from src.preprocessing.normalizer import TextNormalizer


def test_text_cleaner():
    cleaner = TextCleaner()
    text = "Check out https://example.com and email@test.com!!!"
    cleaned = cleaner.clean(text)
    assert "https://example.com" not in cleaned
    assert "email@test.com" not in cleaned


def test_normalizer():
    normalizer = TextNormalizer()
    text = "Hello—world with   spaces"
    normalized = normalizer.normalize(text)
    assert "  " not in normalized
    assert "—" not in normalized
