"""Kafka producer for streaming articles."""

import json
from typing import Optional

from kafka import KafkaProducer
from src.ingestion.schemas import NewsArticle
from src.utils.config import get_config
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ArticleProducer:
    """Kafka producer for news articles."""

    def __init__(self, bootstrap_servers: Optional[str] = None, topic: Optional[str] = None):
        config = get_config()
        self.bootstrap_servers = bootstrap_servers or config.get(
            "ingestion.kafka.bootstrap_servers", "localhost:9092"
        )
        self.topic = topic or config.get("ingestion.kafka.topic", "news-articles")

        self.producer = KafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v, default=str).encode("utf-8"),
            key_serializer=lambda k: k.encode("utf-8") if k else None,
            acks="all",
            retries=3,
            linger_ms=10,
        )
        logger.info(f"Kafka producer initialized: {self.bootstrap_servers}, topic={self.topic}")

    def send_article(self, article: NewsArticle, key: Optional[str] = None) -> None:
        try:
            future = self.producer.send(
                self.topic,
                key=key or article.id,
                value=article.model_dump(mode="json"),
            )
            record_metadata = future.get(timeout=10)
            logger.debug(
                f"Sent article to {record_metadata.topic} "
                f"partition {record_metadata.partition} offset {record_metadata.offset}"
            )
        except Exception as e:
            logger.error(f"Failed to send article to Kafka: {e}")
            raise

    def flush(self) -> None:
        self.producer.flush()

    def close(self) -> None:
        self.producer.close()
