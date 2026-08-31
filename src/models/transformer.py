"""Transformer-based fake news detection model."""
from typing import Dict, List, Optional

import numpy as np
import torch
from sklearn.metrics import accuracy_score, f1_score
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
)


class TransformerModel:
    """HuggingFace transformer wrapper."""

    def __init__(
        self,
        model_name: str = "roberta-base",
        num_labels: int = 2,
        max_length: int = 512,
        device: Optional[str] = None,
    ):
        self.model_name = model_name
        self.max_length = max_length
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_name,
            num_labels=num_labels,
        ).to(self.device)

    def tokenize(self, texts: List[str]) -> Dict:
        return self.tokenizer(
            texts,
            truncation=True,
            padding=True,
            max_length=self.max_length,
            return_tensors="pt",
        )

    def train(
        self,
        train_texts: List[str],
        train_labels: List[int],
        val_texts: Optional[List[str]] = None,
        val_labels: Optional[List[int]] = None,
        output_dir: str = "models/transformer",
        num_epochs: int = 3,
        batch_size: int = 16,
        learning_rate: float = 2e-5,
    ) -> None:
        train_encodings = self.tokenize(train_texts)
        train_encodings["labels"] = torch.tensor(train_labels)

        class FakeNewsDataset(torch.utils.data.Dataset):
            def __init__(self, encodings):
                self.encodings = encodings

            def __getitem__(self, idx):
                return {key: val[idx] for key, val in self.encodings.items()}

            def __len__(self):
                return len(self.encodings["input_ids"])

        train_dataset = FakeNewsDataset(train_encodings)

        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=num_epochs,
            per_device_train_batch_size=batch_size,
            per_device_eval_batch_size=batch_size * 2,
            learning_rate=learning_rate,
            weight_decay=0.01,
            logging_dir=f"{output_dir}/logs",
            logging_steps=100,
            eval_strategy="epoch" if val_texts else "no",
            save_strategy="epoch",
            load_best_model_at_end=True if val_texts else False,
            metric_for_best_model="f1",
        )

        def compute_metrics(eval_pred):
            logits, labels = eval_pred
            predictions = np.argmax(logits, axis=-1)
            return {
                "accuracy": accuracy_score(labels, predictions),
                "f1": f1_score(labels, predictions, average="macro"),
            }

        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=None,
            compute_metrics=compute_metrics,
        )

        trainer.train()
        self.model.save_pretrained(output_dir)
        self.tokenizer.save_pretrained(output_dir)

    def predict(self, texts: List[str]) -> np.ndarray:
        self.model.eval()
        encodings = self.tokenize(texts)
        encodings = {k: v.to(self.device) for k, v in encodings.items()}

        with torch.no_grad():
            outputs = self.model(**encodings)
            logits = outputs.logits
            predictions = torch.argmax(logits, dim=-1)

        return predictions.cpu().numpy()

    def predict_proba(self, texts: List[str]) -> np.ndarray:
        self.model.eval()
        encodings = self.tokenize(texts)
        encodings = {k: v.to(self.device) for k, v in encodings.items()}

        with torch.no_grad():
            outputs = self.model(**encodings)
            probs = torch.softmax(outputs.logits, dim=-1)

        return probs.cpu().numpy()
