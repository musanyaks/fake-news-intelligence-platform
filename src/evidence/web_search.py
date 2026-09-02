"""Web evidence retrieval for claim verification."""
import os
from typing import Dict, List, Optional
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup

from src.utils.logger import get_logger

logger = get_logger(__name__)


class WebEvidenceRetriever:
    """Retrieve web evidence related to a claim."""

    def __init__(self, search_api_key: Optional[str] = None, search_engine_id: Optional[str] = None):
        self.api_key = search_api_key or os.getenv("GOOGLE_SEARCH_API_KEY")
        self.cx = search_engine_id or os.getenv("GOOGLE_SEARCH_ENGINE_ID")
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "TruthLens/1.0 (Fact-Checking Bot)"
        })

    def search(self, claim: str, num_results: int = 5) -> Dict:
        """Search the web for evidence about a claim.

        Returns:
            Dict with search results and source analysis
        """
        results = {
            "results": [],
            "count": 0,
            "source_diversity": 0,
            "has_official_source": False,
            "has_news_coverage": False,
        }

        if not self.api_key or not self.cx:
            logger.warning("Search API not configured. Using fallback.")
            return results

        try:
            search_results = self._google_search(claim, num_results)
            analyzed = []

            for item in search_results:
                analysis = self._analyze_source(item)
                analyzed.append({
                    **item,
                    "credibility_hints": analysis,
                })

                if analysis.get("is_official", False):
                    results["has_official_source"] = True
                if analysis.get("is_news", False):
                    results["has_news_coverage"] = True

            results["results"] = analyzed
            results["count"] = len(analyzed)
            results["source_diversity"] = len(set(
                r.get("domain", "") for r in analyzed
            ))

        except PermissionError as e:
            logger.error(f"Web search permission denied: {e}")
            logger.info("Using mock web evidence fallback.")
            results = self._mock_search(claim)
        except Exception as e:
            logger.error(f"Web search failed: {e}")

        return results

    def _mock_search(self, claim: str) -> Dict:
        """Return realistic mock evidence when APIs are unavailable."""
        claim_lower = claim.lower()

        # Known false claims
        false_claims = [
            "earth is flat", "vaccine microchip", "5g causes", "covid hoax",
            "fake moon landing", "chemtrails", "lizard people", "flat earth",
        ]
        # Known true claims
        true_claims = [
            "study shows", "researchers found", "according to nasa",
            "peer reviewed", "published in nature", "who recommends",
        ]

        is_likely_false = any(fc in claim_lower for fc in false_claims)
        is_likely_true = any(tc in claim_lower for tc in true_claims)

        mock_results = []
        if is_likely_false:
            mock_results = [
                {
                    "title": f"Fact Check: {claim[:50]}...",
                    "url": "https://snopes.com/fact-check/example",
                    "snippet": "Multiple fact-checkers have debunked this claim.",
                    "domain": "snopes.com",
                    "source": "snopes.com",
                    "credibility_hints": {"is_official": False, "is_news": False, "has_factcheck_marker": True, "domain_category": "other"},
                },
            ]
        elif is_likely_true:
            mock_results = [
                {
                    "title": f"Research confirms: {claim[:50]}...",
                    "url": "https://reuters.com/science/research",
                    "snippet": "A new study published in a peer-reviewed journal supports this.",
                    "domain": "reuters.com",
                    "source": "reuters.com",
                    "credibility_hints": {"is_official": False, "is_news": True, "has_factcheck_marker": False, "domain_category": "news"},
                },
            ]
        else:
            mock_results = [
                {
                    "title": f"Search results for: {claim[:50]}...",
                    "url": "https://example.com/search",
                    "snippet": "Limited reliable sources found for this claim.",
                    "domain": "example.com",
                    "source": "example.com",
                    "credibility_hints": {"is_official": False, "is_news": False, "has_factcheck_marker": False, "domain_category": "other"},
                },
            ]

        return {
            "results": mock_results,
            "count": len(mock_results),
            "source_diversity": len(set(r["domain"] for r in mock_results)),
            "has_official_source": any(r["credibility_hints"]["is_official"] for r in mock_results),
            "has_news_coverage": any(r["credibility_hints"]["is_news"] for r in mock_results),
            "mock": True,
        }

    def _google_search(self, query: str, num: int) -> List[Dict]:
        """Perform Google Custom Search."""
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": self.api_key,
            "cx": self.cx,
            "q": query[:500],
            "num": min(num, 10),
        }

        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 403:
            err = response.json().get("error", {}).get("message", "Unknown 403 error")
            logger.error(f"Google Search API 403: {err}. Check billing/API key restrictions at https://console.cloud.google.com/apis/credentials")
            raise PermissionError(f"Google Search API denied: {err}")
        response.raise_for_status()
        data = response.json()

        results = []
        for item in data.get("items", []):
            from urllib.parse import urlparse
            domain = urlparse(item.get("link", "")).netloc
            results.append({
                "title": item.get("title", ""),
                "url": item.get("link", ""),
                "snippet": item.get("snippet", ""),
                "domain": domain,
                "source": item.get("displayLink", domain),
            })

        return results

    def _analyze_source(self, result: Dict) -> Dict:
        """Analyze credibility hints for a search result."""
        domain = result.get("domain", "").lower()
        title = result.get("title", "").lower()

        # Official/government sources
        official_tlds = [".go.ke", ".gov", ".org", ".ac.ke", ".edu"]
        is_official = any(domain.endswith(tld) for tld in official_tlds)

        # News sources
        news_domains = [
            "nation.africa", "standardmedia.co.ke", "the-star.co.ke",
            "citizentv.co.ke", "ntv.co.ke", "kbc.co.ke", "bbc.com",
            "reuters.com", "apnews.com", "aljazeera.com", "cnn",
            "guardian", "nytimes.com", "washingtonpost.com",
        ]
        is_news = any(nd in domain for nd in news_domains)

        # Check for fact-check markers in title
        factcheck_markers = ["fact check", "fact-check", "verdict", "false", "misleading", "true"]
        has_factcheck_marker = any(m in title for m in factcheck_markers)

        return {
            "is_official": is_official,
            "is_news": is_news,
            "has_factcheck_marker": has_factcheck_marker,
            "domain_category": "official" if is_official else ("news" if is_news else "other"),
        }

    def fetch_page_content(self, url: str, max_chars: int = 3000) -> Optional[str]:
        """Fetch and extract text content from a URL."""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "lxml")

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            text = soup.get_text(separator="\n", strip=True)
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            text = "\n".join(lines)

            return text[:max_chars]
        except Exception as e:
            logger.warning(f"Failed to fetch {url}: {e}")
            return None
