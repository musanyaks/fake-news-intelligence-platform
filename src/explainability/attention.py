"""Attention-based explainability for transformers."""
from typing import Dict, List

import numpy as np
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer


class AttentionExplainer:
    """Extract and visualize attention weights."""

    def __init__(self, model_name: str):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_name, output_attentions=True
        )

    def get_attention(self, text: str, layer: int = -1, head: int = 0) -> Dict:
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        tokens = self.tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])

        with torch.no_grad():
            outputs = self.model(**inputs)

        attentions = outputs.attentions[layer][0, head].numpy()

        return {
            "tokens": tokens,
            "attention_matrix": attentions.tolist(),
            "token_importance": attentions.mean(axis=0).tolist(),
        }

    def get_top_attended_tokens(self, text: str, top_k: int = 5) -> List[Dict]:
        result = self.get_attention(text)
        tokens = result["tokens"]
        importance = np.array(result["token_importance"])

        mask = [
            not t.startswith("<") and t not in ["[CLS]", "[SEP]", "</s>", "<s>"]
            for t in tokens
        ]
        filtered_importance = importance[mask]
        filtered_tokens = [t for t, m in zip(tokens, mask) if m]

        top_indices = np.argsort(filtered_importance)[-top_k:][::-1]
        return [
            {"token": filtered_tokens[i], "score": float(filtered_importance[i])}
            for i in top_indices
        ]
