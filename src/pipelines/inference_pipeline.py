"""Real-time inference pipeline."""

from typing import Dict, List

import numpy as np

from src.explainability.attention import AttentionExplainer
from src.preprocessing.cleaner import TextCleaner
from src.preprocessing.normalizer import TextNormalizer
from src.models.transformer import TransformerModel
from src.utils.logger import get_logger

logger = get_logger(__name__)


class InferencePipeline:
    """Production inference pipeline."""

    def __init__(
        self,
        model_path: str = "models/transformer",
        enable_explanation: bool = True,
    ):
        self.cleaner = TextCleaner()
        self.normalizer = TextNormalizer()
        self.model = TransformerModel(model_name=model_path)
        self.enable_explanation = enable_explanation
        self.explainer = None

        if enable_explanation:
            try:
                self.explainer = AttentionExplainer(model_path)
            except Exception as e:
                logger.warning(f"Could not load explainer: {e}")

    def preprocess(self, text: str) -> str:
        text = self.normalizer.normalize(text)
        text = self.cleaner.clean(text)
        return text

    def predict(self, text: str) -> Dict:
        processed = self.preprocess(text)
        proba = self.model.predict_proba([processed])[0]
        prediction = int(np.argmax(proba))
        confidence = float(proba[prediction])

        result = {
            "prediction": prediction,
            "label": "FAKE" if prediction == 1 else "REAL",
            "confidence": confidence,
            "probabilities": {
                "REAL": float(proba[0]),
                "FAKE": float(proba[1]),
            },
        }

        if self.enable_explanation and self.explainer:
            try:
                explanation = self.explainer.get_top_attended_tokens(processed, top_k=5)
                result["explanation"] = explanation
            except Exception as e:
                logger.warning(f"Explanation failed: {e}")

        return result

    def predict_batch(self, texts: List[str]) -> List[Dict]:
        processed = [self.preprocess(t) for t in texts]
        probas = self.model.predict_proba(processed)

        results = []
        for proba in probas:
            prediction = int(np.argmax(proba))
            results.append(
                {
                    "prediction": prediction,
                    "label": "FAKE" if prediction == 1 else "REAL",
                    "confidence": float(proba[prediction]),
                    "probabilities": {"REAL": float(proba[0]), "FAKE": float(proba[1])},
                }
            )
        return results
