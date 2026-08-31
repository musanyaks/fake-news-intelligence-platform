"""Text cleaning utilities."""
import re
import string
from typing import Optional

import nltk
from bs4 import BeautifulSoup

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords", quiet=True)

from nltk.corpus import stopwords


class TextCleaner:
    """Configurable text cleaner."""

    def __init__(
        self,
        lowercase: bool = True,
        remove_urls: bool = True,
        remove_emails: bool = True,
        remove_mentions: bool = True,
        remove_hashtags: bool = False,
        remove_punctuation: bool = False,
        remove_numbers: bool = False,
        remove_extra_whitespace: bool = True,
        remove_stopwords: bool = False,
        min_token_length: int = 2,
        max_token_length: int = 50,
    ):
        self.lowercase = lowercase
        self.remove_urls = remove_urls
        self.remove_emails = remove_emails
        self.remove_mentions = remove_mentions
        self.remove_hashtags = remove_hashtags
        self.remove_punctuation = remove_punctuation
        self.remove_numbers = remove_numbers
        self.remove_extra_whitespace = remove_extra_whitespace
        self.remove_stopwords = remove_stopwords
        self.min_token_length = min_token_length
        self.max_token_length = max_token_length
        self.stop_words = set(stopwords.words("english")) if remove_stopwords else set()

    def clean(self, text: str) -> str:
        if self.lowercase:
            text = text.lower()

        if self.remove_urls:
            text = re.sub(r"https?://\S+|www\.\S+", "", text)

        if self.remove_emails:
            text = re.sub(r"\S+@\S+", "", text)

        if self.remove_mentions:
            text = re.sub(r"@\w+", "", text)

        if self.remove_hashtags:
            text = re.sub(r"#\w+", "", text)

        if self.remove_numbers:
            text = re.sub(r"\d+", "", text)

        if self.remove_punctuation:
            text = text.translate(str.maketrans("", "", string.punctuation))

        if self.remove_stopwords:
            tokens = text.split()
            tokens = [t for t in tokens if t.lower() not in self.stop_words]
            text = " ".join(tokens)

        if self.remove_extra_whitespace:
            text = " ".join(text.split())

        tokens = text.split()
        tokens = [
            t for t in tokens if self.min_token_length <= len(t) <= self.max_token_length
        ]
        text = " ".join(tokens)

        return text.strip()

    @staticmethod
    def strip_html(html: str) -> str:
        soup = BeautifulSoup(html, "lxml")
        return soup.get_text(separator=" ", strip=True)
