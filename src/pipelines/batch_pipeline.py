"""Batch processing pipeline for large datasets."""

import pandas as pd

from src.pipelines.inference_pipeline import InferencePipeline
from src.utils.logger import get_logger

logger = get_logger(__name__)


class BatchPipeline:
    """Process large datasets in batches."""

    def __init__(self, model_path: str = "models/transformer", batch_size: int = 32):
        self.inference = InferencePipeline(model_path=model_path, enable_explanation=False)
        self.batch_size = batch_size

    def process(self, df: pd.DataFrame, text_column: str = "text") -> pd.DataFrame:
        logger.info(f"Processing {len(df)} records in batches of {self.batch_size}")

        results = []
        for i in range(0, len(df), self.batch_size):
            batch = df[text_column].iloc[i : i + self.batch_size].tolist()
            batch_results = self.inference.predict_batch(batch)
            results.extend(batch_results)

        df["prediction"] = [r["prediction"] for r in results]
        df["predicted_label"] = [r["label"] for r in results]
        df["confidence"] = [r["confidence"] for r in results]
        df["prob_real"] = [r["probabilities"]["REAL"] for r in results]
        df["prob_fake"] = [r["probabilities"]["FAKE"] for r in results]

        return df
