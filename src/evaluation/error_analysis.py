"""Error analysis utilities."""
from typing import Dict, List

import numpy as np
import pandas as pd


class ErrorAnalyzer:
    """Analyze model errors."""

    def __init__(
        self, texts: List[str], y_true: np.ndarray, y_pred: np.ndarray, y_proba: np.ndarray
    ):
        self.df = pd.DataFrame({
            "text": texts,
            "y_true": y_true,
            "y_pred": y_pred,
            "confidence": np.max(y_proba, axis=1),
            "correct": y_true == y_pred,
        })

    def get_misclassified(self, n: int = 10) -> pd.DataFrame:
        misclassified = self.df[~self.df["correct"]].copy()
        misclassified["error_type"] = misclassified.apply(
            lambda row: "false_positive" if row["y_pred"] == 1 else "false_negative",
            axis=1,
        )
        return misclassified.nlargest(n, "confidence")

    def get_confidence_distribution(self) -> Dict[str, List[float]]:
        return {
            "correct": self.df[self.df["correct"]]["confidence"].tolist(),
            "incorrect": self.df[~self.df["correct"]]["confidence"].tolist(),
        }

    def analyze_by_length(self) -> pd.DataFrame:
        self.df["text_length"] = self.df["text"].str.len()
        self.df["length_bin"] = pd.cut(self.df["text_length"], bins=5)
        return self.df.groupby("length_bin")["correct"].mean().reset_index()
