"""Metadata feature extraction."""

from typing import Any, Dict, List, Optional

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class MetadataFeatureExtractor(BaseEstimator, TransformerMixin):
    """Extract metadata-based features."""

    def __init__(self) -> None:
        self.source_credibility_db = self._load_credibility_db()

    def _load_credibility_db(self) -> Dict[str, float]:
        return {
            "bbc.com": 0.95,
            "cnn.com": 0.90,
            "nytimes.com": 0.92,
            "reuters.com": 0.95,
            "unknown": 0.50,
        }

    def fit(self, X: Any, y: Optional[Any] = None) -> "MetadataFeatureExtractor":
        return self

    def transform(self, records: List[Dict]) -> np.ndarray:
        features = []
        for record in records:
            source = record.get("source", "unknown")
            domain = source.lower().replace("www.", "")

            credibility = self.source_credibility_db.get(domain, 0.50)

            has_author = 1.0 if record.get("author") else 0.0
            title_length = len(record.get("title", ""))
            content_length = len(record.get("content", ""))
            title_content_ratio = title_length / max(content_length, 1)

            features.append(
                [
                    credibility,
                    has_author,
                    title_length,
                    content_length,
                    title_content_ratio,
                ]
            )
        return np.array(features)

    def get_feature_names(self) -> List[str]:
        return [
            "source_credibility",
            "has_author",
            "title_length",
            "content_length",
            "title_content_ratio",
        ]
