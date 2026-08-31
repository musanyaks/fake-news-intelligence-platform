"""Linguistic feature extraction."""
from typing import List

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class LinguisticFeatureExtractor(BaseEstimator, TransformerMixin):
    """Extract linguistic features from text."""

    def __init__(self):
        self.nlp = None
        self._spacy_available = False
        try:
            import spacy
            self.nlp = spacy.load("en_core_web_sm")
            self._spacy_available = True
        except (ImportError, OSError):
            pass

    def fit(self, X, y=None):
        return self

    def transform(self, texts: List[str]) -> np.ndarray:
        features = []
        for text in texts:
            features.append(self._extract(text))
        return np.array(features)

    def _extract(self, text: str) -> List[float]:
        if self._spacy_available and self.nlp:
            doc = self.nlp(text[:100000])
            words = [token.text.lower() for token in doc if token.is_alpha]
            sentences = list(doc.sents)
            punct_count = sum(1 for token in doc if token.is_punct)
            all_caps_words = sum(1 for token in doc if token.is_alpha and token.text.isupper())
        else:
            words = text.lower().split()
            sentences = text.split(".")
            punct_count = sum(1 for c in text if c in ".,;:!?")
            all_caps_words = sum(1 for w in words if w.isupper() and w.isalpha())

        unique_words = set(words)
        lexical_diversity = len(unique_words) / max(len(words), 1)

        avg_sentence_length = sum(len(s) for s in sentences) / max(len(sentences), 1)
        max_sentence_length = max((len(s) for s in sentences), default=0)

        punct_ratio = punct_count / max(len(text), 1)
        caps_count = sum(1 for c in text if c.isupper())
        caps_ratio = caps_count / max(len(text), 1)
        all_caps_ratio = all_caps_words / max(len(words), 1)

        try:
            import textstat
            flesch_reading = textstat.flesch_reading_ease(text)
            flesch_kincaid = textstat.flesch_kincaid_grade(text)
            gunning_fog = textstat.gunning_fog(text)
            smog = textstat.smog_index(text)
            automated_readability = textstat.automated_readability_index(text)
        except (ImportError, ValueError):
            flesch_reading = 50.0
            flesch_kincaid = 10.0
            gunning_fog = 12.0
            smog = 10.0
            automated_readability = 10.0

        return [
            flesch_reading,
            flesch_kincaid,
            gunning_fog,
            smog,
            automated_readability,
            lexical_diversity,
            avg_sentence_length,
            max_sentence_length,
            punct_ratio,
            caps_ratio,
            all_caps_ratio,
            len(sentences),
            len(words),
        ]

    def get_feature_names(self) -> List[str]:
        return [
            "flesch_reading_ease",
            "flesch_kincaid_grade",
            "gunning_fog",
            "smog_index",
            "automated_readability_index",
            "lexical_diversity",
            "avg_sentence_length",
            "max_sentence_length",
            "punctuation_ratio",
            "capitalization_ratio",
            "all_caps_ratio",
            "num_sentences",
            "num_words",
        ]
