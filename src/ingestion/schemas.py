"""Data schemas for ingestion pipeline."""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl


class NewsArticle(BaseModel):
    id: Optional[str] = None
    title: str = Field(..., min_length=1, max_length=500)
    content: str = Field(..., min_length=10)
    summary: Optional[str] = None
    author: Optional[str] = None
    source: str
    source_url: HttpUrl
    published_at: Optional[datetime] = None
    scraped_at: datetime = Field(default_factory=datetime.utcnow)
    language: Optional[str] = "en"
    category: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Breaking News",
                "content": "This is the article content...",
                "source": "BBC",
                "source_url": "https://www.bbc.com/news/article",
            }
        }


class RawDocument(BaseModel):
    raw_html: Optional[str] = None
    extracted_text: str
    url: HttpUrl
    headers: dict = Field(default_factory=dict)
    status_code: Optional[int] = None
    scraped_at: datetime = Field(default_factory=datetime.utcnow)
