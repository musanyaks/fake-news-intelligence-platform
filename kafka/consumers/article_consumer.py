"""Kafka consumer for processing articles."""
import json

from kafka import KafkaConsumer

from src.pipelines.inference_pipeline import InferencePipeline
from src.utils.logger import get_logger

logger = get_logger(__name__)


def main():
    consumer = KafkaConsumer(
        "news-articles",
        bootstrap_servers="localhost:9092",
        group_id="fake-news-consumer",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset="earliest",
    )

    pipeline = InferencePipeline()

    logger.info("Starting Kafka consumer...")
    for message in consumer:
        article = message.value
        logger.info(f"Processing article: {article.get('title', 'Unknown')}")

        try:
            result = pipeline.predict(article["content"])
            logger.info(f"Prediction: {result['label']} (confidence: {result['confidence']:.3f})")
        except Exception as e:
            logger.error(f"Failed to process article: {e}")


if __name__ == "__main__":
    main()
