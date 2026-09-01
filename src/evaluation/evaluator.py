"""Model evaluation orchestrator."""

from typing import Any, Dict, List, Optional

import numpy as np

from src.evaluation.metrics import compute_metrics, compute_per_class_metrics


class ModelEvaluator:
    """Comprehensive model evaluator."""

    def __init__(self, class_names: Optional[List[str]] = None) -> None:
        self.class_names = class_names or ["REAL", "FAKE"]
        self.results: Dict[str, Dict[str, Any]] = {}

    def evaluate(
        self,
        model_name: str,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        y_proba: Optional[np.ndarray] = None,
    ) -> Dict[str, Any]:
        metrics = compute_metrics(y_true, y_pred, y_proba)
        per_class = compute_per_class_metrics(y_true, y_pred, self.class_names)

        result: Dict[str, Any] = {
            "model": model_name,
            "metrics": metrics,
            "per_class": per_class,
            "sample_size": len(y_true),
        }

        self.results[model_name] = result
        return result

    def compare_models(self) -> Dict[str, Any]:
        if not self.results:
            return {}

        comparison: Dict[str, Dict[str, float]] = {}
        for metric in ["accuracy", "f1_macro", "precision_macro", "recall_macro"]:
            comparison[metric] = {
                name: res["metrics"].get(metric, 0) for name, res in self.results.items()
            }

        return comparison

    def get_best_model(self, metric: str = "f1_macro") -> Optional[str]:
        best_score = -1.0
        best_model: Optional[str] = None
        for name, res in self.results.items():
            score = res["metrics"].get(metric, 0)
            if score > best_score:
                best_score = score
                best_model = name
        return best_model
