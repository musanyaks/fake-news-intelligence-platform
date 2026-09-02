"""Evidence engine module."""
from .fact_check import FactCheckSearcher
from .web_search import WebEvidenceRetriever

__all__ = ["FactCheckSearcher", "WebEvidenceRetriever"]
