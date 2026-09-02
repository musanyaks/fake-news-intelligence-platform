"""Offline mock transformer for development — no downloads needed."""
import random
import re
from typing import Dict, List

import numpy as np


class MockTransformerModel:
    """Deterministic mock model that returns predictions based on text heuristics.
    No internet required. Swap for a real TransformerModel in production.
    """

    FAKE_KEYWORDS = [
        "shocking", "viral", "you won't believe", "doctors hate", "secret",
        "conspiracy", "cover up", "cover-up", "they don't want", "mainstream media hides",
        "wake up", "sheeple", "plandemic", "fake news", "hoax", "scam",
        "banned", "censored", "exposed", "truth about", "what they",
        "urgent", "breaking", "must watch", "share before", "deleted",
        "nobody is talking about", "what really happened", "the real reason",
        "hiding the truth", "hiding", "don't want you to know",
        "flat earth", "earth is flat", "vaccine microchip", "microchip",
        "5g causes", "covid hoax", "fake moon", "moon landing fake",
        "chemtrails", "lizard people", "reptilian", "illuminati",
        "nasa is hiding", "government hiding", "suppressed",
    ]

    REAL_KEYWORDS = [
        "according to", "study shows", "researchers found", "reported by",
        "officials said", "spokesperson confirmed", "data indicates",
        "published in", "peer reviewed", "survey found", "statistics show",
    ]

    def __init__(self, model_name: str = "mock", num_labels: int = 2, **kwargs):
        self.model_name = model_name
        self.num_labels = num_labels
        random.seed(42)

    def _score_text(self, text: str) -> float:
        """Return a score 0-1 where higher = more likely fake."""
        text_lower = text.lower()

        fake_hits = sum(1 for kw in self.FAKE_KEYWORDS if kw in text_lower)
        real_hits = sum(1 for kw in self.REAL_KEYWORDS if kw in text_lower)

        # Base score from keywords (stronger penalty for fake keywords)
        score = 0.40 + (fake_hits * 0.12) - (real_hits * 0.06)

        # Compound effect: multiple fake keywords = much more likely fake
        if fake_hits >= 2:
            score += 0.15
        if fake_hits >= 3:
            score += 0.10

        # Caps lock penalty
        caps_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
        if caps_ratio > 0.3:
            score += 0.1

        # Excessive punctuation
        excl_count = text.count("!")
        if excl_count > 2:
            score += 0.05 * min(excl_count, 5)

        # All-caps words
        words = text.split()
        all_caps = sum(1 for w in words if w.isupper() and len(w) > 2)
        score += 0.03 * min(all_caps, 5)

        # URL in text (slightly more likely real if from known domain)
        if re.search(r"https?://\S+", text):
            score -= 0.02

        return max(0.05, min(0.95, score))

    def predict(self, texts: List[str]) -> np.ndarray:
        return np.array([int(self._score_text(t) > 0.5) for t in texts])

    def predict_proba(self, texts: List[str]) -> np.ndarray:
        scores = [self._score_text(t) for t in texts]
        return np.array([[1 - s, s] for s in scores])

    def train(self, *args, **kwargs):
        pass
