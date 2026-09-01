"""SHAP-based explainability."""

import numpy as np


class ShapExplainer:
    """Wrapper for SHAP explanations."""

    def __init__(self, model, background_data=None):
        self.model = model
        try:
            import shap

            self.explainer = (
                shap.Explainer(model, background_data) if background_data else shap.Explainer(model)
            )
        except ImportError:
            self.explainer = None

    def explain(self, X: np.ndarray):
        if self.explainer is None:
            raise RuntimeError("SHAP not available")
        return self.explainer(X)

    def explain_text(self, text: str, tokenizer, model) -> dict:
        try:
            import shap

            explainer = shap.Explainer(model, tokenizer)
            shap_values = explainer([text])
            return {
                "text": text,
                "shap_values": shap_values.values.tolist(),
                "base_values": shap_values.base_values.tolist(),
            }
        except Exception as e:
            return {"error": str(e)}

    def get_feature_importance(self, X: np.ndarray) -> dict:
        if self.explainer is None:
            return {}
        shap_values = self.explain(X)
        importance = np.abs(shap_values.values).mean(axis=0)
        return {f"feature_{i}": float(v) for i, v in enumerate(importance)}
