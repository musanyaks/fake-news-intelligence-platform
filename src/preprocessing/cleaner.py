"""Text cleaning utilities."""

import re
import string
from typing import Optional

from bs4 import BeautifulSoup


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
        self._stop_words: Optional[set] = None

    @property
    def stop_words(self) -> set:
        if self._stop_words is None:
            try:
                import nltk
                from nltk.corpus import stopwords as nltk_stopwords

                nltk.data.find("corpora/stopwords")
                self._stop_words = set(nltk_stopwords.words("english"))
            except (LookupError, ValueError, ImportError):
                self._stop_words = {
                    "i",
                    "me",
                    "my",
                    "myself",
                    "we",
                    "our",
                    "ours",
                    "ourselves",
                    "you",
                    "your",
                    "yours",
                    "yourself",
                    "yourselves",
                    "he",
                    "him",
                    "his",
                    "himself",
                    "she",
                    "her",
                    "hers",
                    "herself",
                    "it",
                    "its",
                    "itself",
                    "they",
                    "them",
                    "their",
                    "theirs",
                    "themselves",
                    "what",
                    "which",
                    "who",
                    "whom",
                    "this",
                    "that",
                    "these",
                    "those",
                    "am",
                    "is",
                    "are",
                    "was",
                    "were",
                    "be",
                    "been",
                    "being",
                    "have",
                    "has",
                    "had",
                    "having",
                    "do",
                    "does",
                    "did",
                    "doing",
                    "a",
                    "an",
                    "the",
                    "and",
                    "but",
                    "if",
                    "or",
                    "because",
                    "as",
                    "until",
                    "while",
                    "of",
                    "at",
                    "by",
                    "for",
                    "with",
                    "through",
                    "during",
                    "before",
                    "after",
                    "above",
                    "below",
                    "up",
                    "down",
                    "in",
                    "out",
                    "on",
                    "off",
                    "over",
                    "under",
                    "again",
                    "further",
                    "then",
                    "once",
                    "here",
                    "there",
                    "when",
                    "where",
                    "why",
                    "how",
                    "all",
                    "any",
                    "both",
                    "each",
                    "few",
                    "more",
                    "most",
                    "other",
                    "some",
                    "such",
                    "no",
                    "nor",
                    "not",
                    "only",
                    "own",
                    "same",
                    "so",
                    "than",
                    "too",
                    "very",
                    "s",
                    "t",
                    "can",
                    "will",
                    "just",
                    "don",
                    "should",
                    "now",
                }
        return self._stop_words

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
        tokens = [t for t in tokens if self.min_token_length <= len(t) <= self.max_token_length]
        text = " ".join(tokens)

        return text.strip()

    @staticmethod
    def strip_html(html: str) -> str:
        soup = BeautifulSoup(html, "lxml")
        return soup.get_text(separator=" ", strip=True)
