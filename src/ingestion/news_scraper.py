"""News scraper for multiple sources."""

import hashlib
from datetime import datetime
from typing import AsyncGenerator, List, Optional

import aiohttp
import feedparser
from bs4 import BeautifulSoup

from src.ingestion.schemas import NewsArticle, RawDocument
from src.utils.logger import get_logger

logger = get_logger(__name__)


class NewsScraper:
    """Asynchronous news scraper with multiple source support."""

    def __init__(self, timeout: int = 30):
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(timeout=self.timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def fetch_url(self, url: str, headers: Optional[dict] = None) -> RawDocument:
        if not self.session:
            raise RuntimeError("Scraper not initialized. Use async context manager.")

        default_headers = {"User-Agent": "FakeNewsIntelligenceBot/1.0 (Research Project)"}
        if headers:
            default_headers.update(headers)

        try:
            async with self.session.get(url, headers=default_headers) as response:
                html = await response.text()
                soup = BeautifulSoup(html, "lxml")
                text = soup.get_text(separator="\n", strip=True)

                return RawDocument(
                    raw_html=html,
                    extracted_text=text,
                    url=url,
                    headers=dict(response.headers),
                    status_code=response.status,
                )
        except Exception as e:
            logger.error(f"Failed to fetch {url}: {e}")
            raise

    def parse_rss_feed(self, feed_url: str) -> List[NewsArticle]:
        feed = feedparser.parse(feed_url)
        articles = []

        for entry in feed.entries:
            article = NewsArticle(
                id=hashlib.md5(entry.link.encode()).hexdigest(),
                title=entry.get("title", ""),
                content=entry.get("summary", entry.get("description", "")),
                source=feed.feed.get("title", "Unknown"),
                source_url=entry.link,
                published_at=self._parse_date(entry.get("published")),
                author=entry.get("author"),
                tags=[tag.term for tag in entry.get("tags", [])],
            )
            articles.append(article)

        logger.info(f"Parsed {len(articles)} articles from {feed_url}")
        return articles

    async def scrape_article(self, url: str) -> NewsArticle:
        doc = await self.fetch_url(url)
        soup = BeautifulSoup(doc.raw_html or doc.extracted_text, "lxml")

        title = soup.find("title")
        title_text = title.get_text(strip=True) if title else ""

        article_body = soup.find("article") or soup.find("main") or soup.find("body")
        content = (
            article_body.get_text(separator="\n", strip=True)
            if article_body
            else doc.extracted_text
        )

        return NewsArticle(
            id=hashlib.md5(url.encode()).hexdigest(),
            title=title_text,
            content=content,
            source=url.split("/")[2],
            source_url=url,
            scraped_at=datetime.utcnow(),
        )

    async def scrape_multiple(self, urls: List[str]) -> AsyncGenerator[NewsArticle, None]:
        for url in urls:
            try:
                article = await self.scrape_article(url)
                yield article
            except Exception as e:
                logger.warning(f"Skipping {url}: {e}")
                continue

    @staticmethod
    def _parse_date(date_str: Optional[str]) -> Optional[datetime]:
        if not date_str:
            return None
        try:
            return datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")
        except ValueError:
            try:
                return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S%z")
            except ValueError:
                return None
