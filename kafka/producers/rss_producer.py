"""RSS feed to Kafka producer."""
import time

from src.ingestion.kafka_producer import ArticleProducer
from src.ingestion.news_scraper import NewsScraper
from src.utils.logger import get_logger

logger = get_logger(__name__)

RSS_FEEDS = [
    "https://feeds.bbci.co.uk/news/rss.xml",
    "https://rss.cnn.com/rss/edition.rss",
]


def main():
    producer = ArticleProducer()
    scraper = NewsScraper()

    logger.info("Starting RSS producer...")
    while True:
        for feed_url in RSS_FEEDS:
            try:
                articles = scraper.parse_rss_feed(feed_url)
                for article in articles:
                    producer.send_article(article)
                producer.flush()
                logger.info(f"Sent {len(articles)} articles from {feed_url}")
            except Exception as e:
                logger.error(f"Error processing {feed_url}: {e}")

        time.sleep(300)  # Poll every 5 minutes


if __name__ == "__main__":
    main()
