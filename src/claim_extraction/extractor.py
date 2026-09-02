"""Claim extraction from text, URLs, and images."""
import re
from typing import Dict, List, Optional
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from src.preprocessing.cleaner import TextCleaner
from src.preprocessing.normalizer import TextNormalizer
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ClaimExtractor:
    """Extract factual claims from various input types."""

    def __init__(self):
        self.cleaner = TextCleaner(
            lowercase=False,
            remove_urls=False,
            remove_emails=True,
            remove_mentions=True,
            remove_hashtags=False,
            remove_punctuation=False,
            remove_numbers=False,
        )
        self.normalizer = TextNormalizer()
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "TruthLens/1.0 (Fact-Checking Bot; https://truthlens.example)"
        })

    def extract(self, query: str, query_type: str = "text") -> Dict:
        """Extract claims from input.

        Args:
            query: The input string (text, URL, or image path)
            query_type: One of "text", "url", "image"

        Returns:
            Dict with extracted claims and metadata
        """
        if query_type == "url":
            return self._extract_from_url(query)
        elif query_type == "image":
            return self._extract_from_image(query)
        else:
            return self._extract_from_text(query)

    def _extract_from_text(self, text: str) -> Dict:
        """Extract claims from raw text or forwarded messages."""
        normalized = self.normalizer.normalize(text)
        cleaned = self.cleaner.clean(normalized)

        # Split into sentences/claims
        claims = self._split_into_claims(cleaned)

        # Identify the primary claim (usually the first substantial one)
        primary_claim = self._identify_primary_claim(claims)

        return {
            "input_type": "text",
            "original_text": text,
            "cleaned_text": cleaned,
            "claims": claims,
            "primary_claim": primary_claim,
            "claim_count": len(claims),
            "metadata": {
                "word_count": len(cleaned.split()),
                "has_url": bool(re.search(r"https?://\S+|www\.\S+", text)),
                "has_numbers": bool(re.search(r"\d+", text)),
            },
        }

    def _extract_from_url(self, url: str) -> Dict:
        """Fetch and extract claims from a URL."""
        try:
            parsed = urlparse(url)
            if not parsed.scheme:
                url = "https://" + url

            response = self.session.get(url, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "lxml")

            # Extract article content
            article = self._parse_article(soup, url)

            # Extract claims from article text
            text_result = self._extract_from_text(article["text"])

            return {
                "input_type": "url",
                "url": url,
                "article": article,
                **text_result,
                "metadata": {
                    **text_result.get("metadata", {}),
                    "domain": parsed.netloc,
                    "title": article.get("title", ""),
                    "author": article.get("author", ""),
                    "publish_date": article.get("publish_date", ""),
                },
            }

        except Exception as e:
            logger.error(f"Failed to extract from URL {url}: {e}")
            return {
                "input_type": "url",
                "url": url,
                "error": str(e),
                "claims": [],
                "primary_claim": None,
            }

    def _extract_from_image(self, image_path: str) -> Dict:
        """Extract text from image using OCR."""
        try:
            import pytesseract
            from PIL import Image

            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)

            text_result = self._extract_from_text(text)

            return {
                "input_type": "image",
                "image_path": image_path,
                **text_result,
            }

        except ImportError:
            logger.warning("OCR dependencies not installed. Returning empty.")
            return {
                "input_type": "image",
                "image_path": image_path,
                "error": "OCR not available",
                "claims": [],
                "primary_claim": None,
            }
        except Exception as e:
            logger.error(f"OCR failed for {image_path}: {e}")
            return {
                "input_type": "image",
                "image_path": image_path,
                "error": str(e),
                "claims": [],
                "primary_claim": None,
            }

    def _parse_article(self, soup: BeautifulSoup, url: str) -> Dict:
        """Parse article metadata and content from HTML."""
        # Try to get title
        title = ""
        if soup.title:
            title = soup.title.get_text(strip=True)
        for meta in soup.find_all("meta", property="og:title"):
            title = meta.get("content", title)

        # Try to get author
        author = ""
        for meta in soup.find_all("meta", attrs={"name": "author"}):
            author = meta.get("content", author)
        for meta in soup.find_all("meta", property="og:author"):
            author = meta.get("content", author)

        # Try to get publish date
        publish_date = ""
        for meta in soup.find_all("meta", property="article:published_time"):
            publish_date = meta.get("content", publish_date)

        # Extract main text content
        text = ""

        # Try common article containers
        for selector in ["article", "main", ".article-content", ".post-content",
                         ".entry-content", "[role='main']"]:
            container = soup.select_one(selector)
            if container:
                text = container.get_text(separator="\n", strip=True)
                break

        # Fallback to all paragraphs
        if not text:
            paragraphs = soup.find_all("p")
            text = "\n".join(p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 30)

        # Clean up
        text = self.normalizer.normalize(text)

        return {
            "title": title,
            "author": author,
            "publish_date": publish_date,
            "text": text,
        }

    def _split_into_claims(self, text: str) -> List[str]:
        """Split text into individual factual claims."""
        # Split by sentence boundaries
        sentences = re.split(r'(?<=[.!?])\s+', text)

        claims = []
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 15:
                continue
            # Filter out questions, greetings, etc.
            if sentence.endswith("?"):
                continue
            if sentence.lower().startswith(("hello", "hi ", "hey", "dear ", "thank")):
                continue
            claims.append(sentence)

        return claims

    def _identify_primary_claim(self, claims: List[str]) -> Optional[str]:
        """Identify the most important claim from a list."""
        if not claims:
            return None

        # Heuristic: first substantial claim is usually the main one
        # In forwarded messages, the claim often comes after any greeting
        for claim in claims:
            words = claim.split()
            if len(words) >= 5:
                return claim

        return claims[0] if claims else None
