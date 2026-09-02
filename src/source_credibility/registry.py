"""Source credibility registry and scoring."""
from typing import Dict, List, Optional

from src.utils.logger import get_logger

logger = get_logger(__name__)


class SourceRegistry:
    """Registry of known sources with credibility scores."""

    def __init__(self):
        self.sources = self._load_sources()

    def get_score(self, domain: str) -> Optional[Dict]:
        """Get credibility score for a domain."""
        domain = domain.lower().strip()

        # Exact match
        if domain in self.sources:
            return self.sources[domain]

        # Partial match
        for key, info in self.sources.items():
            if key in domain or domain in key:
                return info

        return None

    def score_url(self, url: str) -> Dict:
        """Score a URL's source credibility."""
        from urllib.parse import urlparse
        domain = urlparse(url).netloc.lower()

        source_info = self.get_score(domain)

        if source_info:
            return {
                "domain": domain,
                "known_source": True,
                "credibility_score": source_info["score"],
                "tier": source_info["tier"],
                "category": source_info["category"],
                "description": source_info.get("description", ""),
                "flags": source_info.get("flags", []),
            }

        # Unknown source
        return {
            "domain": domain,
            "known_source": False,
            "credibility_score": 50,  # Neutral for unknown
            "tier": "unknown",
            "category": "unknown",
            "description": "Source not in registry",
            "flags": ["unknown_source"],
        }

    def _load_sources(self) -> Dict[str, Dict]:
        """Load known sources."""
        return {
            # Tier 1: Highly credible
            "nation.africa": {
                "score": 85,
                "tier": "high",
                "category": "news",
                "description": "Nation Media Group",
                "flags": [],
            },
            "standardmedia.co.ke": {
                "score": 85,
                "tier": "high",
                "category": "news",
                "description": "The Standard",
                "flags": [],
            },
            "the-star.co.ke": {
                "score": 82,
                "tier": "high",
                "category": "news",
                "description": "The Star Kenya",
                "flags": [],
            },
            "citizentv.co.ke": {
                "score": 80,
                "tier": "high",
                "category": "news",
                "description": "Citizen TV Kenya",
                "flags": [],
            },
            "ntv.co.ke": {
                "score": 80,
                "tier": "high",
                "category": "news",
                "description": "NTV Kenya",
                "flags": [],
            },
            "bbc.com": {
                "score": 90,
                "tier": "high",
                "category": "news",
                "description": "BBC News",
                "flags": [],
            },
            "reuters.com": {
                "score": 92,
                "tier": "high",
                "category": "news",
                "description": "Reuters",
                "flags": [],
            },
            "apnews.com": {
                "score": 92,
                "tier": "high",
                "category": "news",
                "description": "Associated Press",
                "flags": [],
            },

            # Tier 2: Fact-checkers
            "africacheck.org": {
                "score": 95,
                "tier": "high",
                "category": "fact_check",
                "description": "Africa Check",
                "flags": [],
            },
            "pesacheck.org": {
                "score": 93,
                "tier": "high",
                "category": "fact_check",
                "description": "PesaCheck",
                "flags": [],
            },
            "factcheck.org": {
                "score": 93,
                "tier": "high",
                "category": "fact_check",
                "description": "FactCheck.org",
                "flags": [],
            },
            "snopes.com": {
                "score": 88,
                "tier": "high",
                "category": "fact_check",
                "description": "Snopes",
                "flags": [],
            },

            # Tier 3: Official/Government
            "go.ke": {
                "score": 88,
                "tier": "high",
                "category": "government",
                "description": "Kenya Government",
                "flags": [],
            },
            "centralbank.go.ke": {
                "score": 90,
                "tier": "high",
                "category": "government",
                "description": "Central Bank of Kenya",
                "flags": [],
            },
            "treasury.go.ke": {
                "score": 90,
                "tier": "high",
                "category": "government",
                "description": "Kenya Treasury",
                "flags": [],
            },
            "iebc.or.ke": {
                "score": 85,
                "tier": "high",
                "category": "government",
                "description": "IEBC Kenya",
                "flags": [],
            },

            # Tier 4: Known low-credibility
            "kenyan-post.com": {
                "score": 25,
                "tier": "low",
                "category": "blog",
                "description": "Known for unverified content",
                "flags": ["unverified", "sensationalist"],
            },
            "credible-source.example": {
                "score": 50,
                "tier": "medium",
                "category": "unknown",
                "description": "Placeholder",
                "flags": [],
            },
        }
