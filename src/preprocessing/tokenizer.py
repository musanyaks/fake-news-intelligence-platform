"""Text tokenization utilities."""

from typing import Any, Dict, List

from transformers import AutoTokenizer


class Tokenizer:
    """Wrapper for HuggingFace tokenizers with fallback."""

    def __init__(
        self,
        model_name: str = "roberta-base",
        max_length: int = 512,
    ) -> None:
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.max_length = max_length

    def encode(self, text: str) -> Dict[str, Any]:
        return dict(
            self.tokenizer(
                text,
                truncation=True,
                padding="max_length",
                max_length=self.max_length,
                return_tensors="pt",
            )
        )

    def encode_batch(self, texts: List[str]) -> Dict[str, Any]:
        return dict(
            self.tokenizer(
                texts,
                truncation=True,
                padding=True,
                max_length=self.max_length,
                return_tensors="pt",
            )
        )

    def decode(
        self,
        token_ids: List[int],
        skip_special_tokens: bool = True,
    ) -> str:
        return str(
            self.tokenizer.decode(
                token_ids,
                skip_special_tokens=skip_special_tokens,
            )
        )

    def tokenize(self, text: str) -> List[str]:
        return self.tokenizer.tokenize(text)
