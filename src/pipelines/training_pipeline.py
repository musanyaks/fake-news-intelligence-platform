"""End-to-end training pipeline."""

from typing import Any, Dict

import mlflow
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from src.evaluation.evaluator import ModelEvaluator
from src.features.feature_pipeline import FeaturePipeline
from src.models.baseline import BaselineModel
from src.models.tfidf_model import TfidfModel
from src.models.transformer import TransformerModel
from src.preprocessing.cleaner import TextCleaner
from src.utils.config import get_config
from src.utils.logger import get_logger

logger = get_logger(__name__)


class TrainingPipeline:
    """Orchestrates model training."""

    def __init__(self, config_path: str = "configs/config.yaml"):
        self.config = get_config()
        self.cleaner = TextCleaner()
        self.evaluator = ModelEvaluator()

    def load_data(self, path: str) -> pd.DataFrame:
        logger.info(f"Loading data from {path}")
        df = pd.read_csv(path)
        return df

    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.info("Preprocessing data")
        df["clean_text"] = df["text"].apply(self.cleaner.clean)
        return df

    def split_data(self, df: pd.DataFrame) -> tuple:
        test_size = self.config.get("training.test_size", 0.2)
        val_size = self.config.get("training.validation_size", 0.1)
        random_state = self.config.get("training.random_state", 42)

        train_df, temp_df = train_test_split(
            df, test_size=test_size + val_size, random_state=random_state, stratify=df["label"]
        )
        val_df, test_df = train_test_split(
            temp_df,
            test_size=test_size / (test_size + val_size),
            random_state=random_state,
            stratify=temp_df["label"],
        )

        return train_df, val_df, test_df

    def train_baseline(
        self, X_train: np.ndarray, y_train: np.ndarray, X_val: np.ndarray, y_val: np.ndarray
    ) -> Dict:
        logger.info("Training baseline model")
        model = BaselineModel(model_type="logistic_regression")
        model.fit(X_train, y_train)
        results = model.evaluate(X_val, y_val)
        return {"model": model, "results": results}

    def train_tfidf(
        self, train_texts: list, y_train: np.ndarray, val_texts: list, y_val: np.ndarray
    ) -> Dict:
        logger.info("Training TF-IDF model")
        model = TfidfModel()
        model.fit(train_texts, y_train)
        results = model.evaluate(val_texts, y_val)
        return {"model": model, "results": results}

    def train_transformer(
        self, train_texts: list, y_train: list, val_texts: list, val_val: list
    ) -> Dict:
        logger.info("Training transformer model")
        model = TransformerModel()
        model.train(train_texts, y_train, val_texts, val_val, output_dir="models/transformer")
        preds = model.predict(val_texts)
        from sklearn.metrics import f1_score, accuracy_score

        results = {
            "accuracy": accuracy_score(val_val, preds),
            "f1": f1_score(val_val, preds, average="macro"),
        }
        return {"model": model, "results": results}

    def run(self, data_path: str) -> Dict[str, Any]:
        mlflow.set_experiment(self.config.get("app.name", "fake-news-detection"))

        with mlflow.start_run():
            df = self.load_data(data_path)
            df = self.preprocess(df)

            train_df, val_df, test_df = self.split_data(df)

            mlflow.log_params(
                {
                    "train_size": len(train_df),
                    "val_size": len(val_df),
                    "test_size": len(test_df),
                }
            )

            feature_pipeline = FeaturePipeline()
            X_train = feature_pipeline.fit_transform(train_df["clean_text"].tolist())
            X_val = feature_pipeline.transform(val_df["clean_text"].tolist())

            baseline = self.train_baseline(
                X_train, train_df["label"].values, X_val, val_df["label"].values
            )
            self.evaluator.evaluate(
                "baseline", val_df["label"].values, baseline["results"]["predictions"]
            )

            tfidf = self.train_tfidf(
                train_df["clean_text"].tolist(),
                train_df["label"].values,
                val_df["clean_text"].tolist(),
                val_df["label"].values,
            )
            self.evaluator.evaluate(
                "tfidf",
                val_df["label"].values,
                tfidf["results"]["predictions"],
                tfidf["results"]["probabilities"],
            )

            self.train_transformer(
                train_df["text"].tolist(),
                train_df["label"].tolist(),
                val_df["text"].tolist(),
                val_df["label"].tolist(),
            )

            comparison = self.evaluator.compare_models()
            logger.info(f"Model comparison: {comparison}")

            for model_name, result in self.evaluator.results.items():
                for k, v in result["metrics"].items():
                    if isinstance(v, (int, float)):
                        mlflow.log_metric(f"{model_name}_{k}", v)

            return self.evaluator.results
