"""Feature pipeline orchestration."""

from typing import Any, List, Optional

import numpy as np
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.preprocessing import StandardScaler

from src.features.linguistic import LinguisticFeatureExtractor
from src.features.sentiment import SentimentFeatureExtractor


class FeaturePipeline:
    """Orchestrates all feature extractors."""

    def __init__(self) -> None:
        self.pipeline = Pipeline(
            [
                (
                    "features",
                    FeatureUnion(
                        [
                            ("linguistic", LinguisticFeatureExtractor()),
                            ("sentiment", SentimentFeatureExtractor()),
                        ]
                    ),
                ),
                ("scaler", StandardScaler()),
            ]
        )

    def fit_transform(self, texts: List[str]) -> np.ndarray:
        return np.asarray(self.pipeline.fit_transform(texts))

    def transform(self, texts: List[str]) -> np.ndarray:
        return np.asarray(self.pipeline.transform(texts))

    def fit(self, texts: List[str], y: Optional[Any] = None) -> "FeaturePipeline":
        self.pipeline.fit(texts, y)
        return self
