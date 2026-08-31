"""Baseline sklearn models."""
from typing import Any, Dict

import numpy as np
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, f1_score


class BaselineModel:
    """Wrapper for traditional ML models."""

    def __init__(self, model_type: str = "logistic_regression", params: Dict[str, Any] = None):
        self.model_type = model_type
        self.params = params or {}
        self.model = self._build_model()

    def _build_model(self):
        if self.model_type == "logistic_regression":
            return LogisticRegression(**self.params)
        elif self.model_type == "random_forest":
            return RandomForestClassifier(**self.params)
        elif self.model_type == "gradient_boosting":
            return GradientBoostingClassifier(**self.params)
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")

    def fit(self, X: np.ndarray, y: np.ndarray) -> "BaselineModel":
        self.model.fit(X, y)
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict(X)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        if hasattr(self.model, "predict_proba"):
            return self.model.predict_proba(X)
        raise AttributeError(f"{self.model_type} does not support probability predictions")

    def evaluate(self, X: np.ndarray, y: np.ndarray) -> Dict[str, Any]:
        predictions = self.predict(X)
        proba = self.predict_proba(X) if hasattr(self.model, "predict_proba") else None

        report = classification_report(y, predictions, output_dict=True)
        f1 = f1_score(y, predictions, average="macro")

        return {
            "f1_macro": f1,
            "classification_report": report,
            "predictions": predictions,
            "probabilities": proba,
        }
