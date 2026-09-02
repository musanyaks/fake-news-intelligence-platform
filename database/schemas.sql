-- Database schema for fake news platform

CREATE TABLE IF NOT EXISTS articles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    external_id VARCHAR(255) UNIQUE,
    title VARCHAR(1000) NOT NULL,
    content TEXT NOT NULL,
    summary TEXT,
    author VARCHAR(255),
    source VARCHAR(255) NOT NULL,
    source_url TEXT NOT NULL,
    published_at TIMESTAMP WITH TIME ZONE,
    scraped_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    language VARCHAR(10) DEFAULT 'en',
    category VARCHAR(100),
    tags TEXT[],
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS predictions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    article_id UUID REFERENCES articles(id),
    model_version VARCHAR(50) NOT NULL,
    prediction INTEGER NOT NULL CHECK (prediction IN (0, 1)),
    confidence DECIMAL(5,4) NOT NULL CHECK (confidence >= 0 AND confidence <= 1),
    prob_real DECIMAL(5,4) NOT NULL,
    prob_fake DECIMAL(5,4) NOT NULL,
    explanation JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS model_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    version VARCHAR(50) UNIQUE NOT NULL,
    model_type VARCHAR(100) NOT NULL,
    artifact_path TEXT NOT NULL,
    metrics JSONB,
    is_active BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_articles_source ON articles(source);
CREATE INDEX idx_articles_scraped_at ON articles(scraped_at);
CREATE INDEX idx_predictions_article_id ON predictions(article_id);
CREATE INDEX idx_predictions_created_at ON predictions(created_at);
