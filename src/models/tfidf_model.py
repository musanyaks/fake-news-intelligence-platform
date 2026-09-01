"""TF-IDF based model."""
from typing import Any, Dict, Optional

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline


class TfidfModel:
    """TF-IDF + linear classifier pipeline."""

    def __init__(
        self,
        max_features: int = 15000,
        ngram_range: tuple = (1, 3),
        classifier_params: Optional[Dict[str, Any]] = None,
    ):
        self.pipeline = Pipeline([
            ("tfidf", TfidfVectorizer(
                max_features=max_features,
                ngram_range=ngram_range,
                min_df=2,
                max_df=0.95,
                sublinear_tf=True,
                strip_accents="unicode",
            )),
            ("clf", SGDClassifier(
                loss="log_loss",
                penalty="elasticnet",
                alpha=0.0001,
                l1_ratio=0.15,
                max_iter=1000,
                tol=0.001,
                class_weight="balanced",
                random_state=42,
            )),
        ])

    def fit(self, texts: list, labels: np.ndarray) -> "TfidfModel":
        self.pipeline.fit(texts, labels)
        return self

    def predict(self, texts: list) -> np.ndarray:
        return np.asarray(self.pipeline.predict(texts))

    def predict_proba(self, texts: list) -> np.ndarray:
        return np.asarray(self.pipeline.predict_proba(texts))

    def evaluate(self, texts: list, labels: np.ndarray) -> Dict[str, Any]:
        from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

        preds = self.predict(texts)
        proba = self.predict_proba(texts)

        return {
            "accuracy": accuracy_score(labels, preds),
            "precision": precision_score(labels, preds, average="macro"),
            "recall": recall_score(labels, preds, average="macro"),
            "f1": f1_score(labels, preds, average="macro"),
            "predictions": preds,
            "probabilities": proba,
        }
