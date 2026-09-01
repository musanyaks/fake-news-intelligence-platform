"""Training script entrypoint."""

import argparse

from src.pipelines.training_pipeline import TrainingPipeline
from src.utils.logger import get_logger, setup_logging

logger = get_logger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(description="Train fake news detection models")
    parser.add_argument("--config", default="configs/config.yaml", help="Path to config file")
    parser.add_argument("--data", default="data/processed/train.csv", help="Path to training data")
    parser.add_argument("--output", default="models/", help="Output directory for models")
    args = parser.parse_args()

    setup_logging()

    pipeline = TrainingPipeline(config_path=args.config)
    results = pipeline.run(args.data)

    logger.info("Training complete")
    for model_name, result in results.items():
        logger.info(f"{model_name}: {result['metrics']}")


if __name__ == "__main__":
    main()
