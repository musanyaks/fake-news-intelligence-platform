"""Sentiment feature extraction."""

from typing import Any, List, Optional

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class SentimentFeatureExtractor(BaseEstimator, TransformerMixin):
    """Extract sentiment features."""

    def __init__(self) -> None:
        self.analyzer = SentimentIntensityAnalyzer()

    def fit(self, X: Any, y: Optional[Any] = None) -> "SentimentFeatureExtractor":
        return self

    def transform(self, texts: List[str]) -> np.ndarray:
        features = []
        for text in texts:
            scores = self.analyzer.polarity_scores(text)
            features.append(
                [
                    scores["neg"],
                    scores["neu"],
                    scores["pos"],
                    scores["compound"],
                    abs(scores["compound"]),
                ]
            )
        return np.array(features)

    def get_feature_names(self) -> List[str]:
        return [
            "sentiment_neg",
            "sentiment_neu",
            "sentiment_pos",
            "sentiment_compound",
            "sentiment_intensity",
        ]
