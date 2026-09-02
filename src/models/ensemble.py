"""Ensemble model combining multiple approaches."""
from typing import Any, Dict, List, Optional

import numpy as np


class EnsembleModel:
    """Weighted voting ensemble."""

    def __init__(
        self,
        models: Dict[str, Any],
        method: str = "voting",
        weights: Optional[Dict[str, float]] = None,
    ):
        self.models = models
        self.method = method
        self.weights = weights

    def fit(self, X_dict: Dict[str, Any], y: np.ndarray) -> "EnsembleModel":
        # Fit each base model on its respective features
        for name, model in self.models.items():
            if hasattr(model, "fit"):
                model.fit(X_dict[name], y)
        return self

    def predict(self, X_dict: Dict[str, Any]) -> np.ndarray:
        predictions = []
        for name, model in self.models.items():
            weight = self.weights.get(name, 1.0) if self.weights else 1.0
            proba = model.predict_proba(X_dict[name])
            predictions.append(proba * weight)

        avg_proba = np.mean(predictions, axis=0)
        return np.argmax(avg_proba, axis=1)

    def predict_proba(self, X_dict: Dict[str, Any]) -> np.ndarray:
        predictions = []
        for name, model in self.models.items():
            weight = self.weights.get(name, 1.0) if self.weights else 1.0
            proba = model.predict_proba(X_dict[name])
            predictions.append(proba * weight)

        total_weight = sum(self.weights.values()) if self.weights else len(self.models)
        return np.sum(predictions, axis=0) / total_weight
