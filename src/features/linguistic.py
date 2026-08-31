"""Linguistic feature extraction."""
from typing import Dict, List

import numpy as np
import spacy
import textstat
from sklearn.base import BaseEstimator, TransformerMixin


class LinguisticFeatureExtractor(BaseEstimator, TransformerMixin):
    """Extract linguistic features from text."""

    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            raise RuntimeError(
                "spaCy model 'en_core_web_sm' not installed. "
                "Run: python -m spacy download en_core_web_sm"
            )

    def fit(self, X, y=None):
        return self

    def transform(self, texts: List[str]) -> np.ndarray:
        features = []
        for text in texts:
            features.append(self._extract(text))
        return np.array(features)

    def _extract(self, text: str) -> List[float]:
        doc = self.nlp(text[:100000])

        flesch_reading = textstat.flesch_reading_ease(text)
        flesch_kincaid = textstat.flesch_kincaid_grade(text)
        gunning_fog = textstat.gunning_fog(text)
        smog = textstat.smog_index(text)
        automated_readability = textstat.automated_readability_index(text)

        words = [token.text.lower() for token in doc if token.is_alpha]
        unique_words = set(words)
        lexical_diversity = len(unique_words) / max(len(words), 1)

        sentences = list(doc.sents)
        avg_sentence_length = np.mean([len(sent) for sent in sentences]) if sentences else 0
        max_sentence_length = max([len(sent) for sent in sentences]) if sentences else 0

        punct_count = sum(1 for token in doc if token.is_punct)
        punct_ratio = punct_count / max(len(doc), 1)

        caps_count = sum(1 for c in text if c.isupper())
        caps_ratio = caps_count / max(len(text), 1)
        all_caps_words = sum(1 for token in doc if token.is_alpha and token.text.isupper())
        all_caps_ratio = all_caps_words / max(len(words), 1)

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
