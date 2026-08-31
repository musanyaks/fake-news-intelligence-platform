# Data Dictionary

## Raw Data

### articles.csv

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| id | string | Unique article identifier | "a1b2c3d4" |
| title | string | Article headline | "Breaking: Major Event Occurs" |
| content | string | Full article text | "Today, officials announced..." |
| author | string | Article author | "Jane Doe" |
| source | string | Publication source | "BBC" |
| source_url | string | Original URL | "https://bbc.com/news/123" |
| published_at | datetime | Publication timestamp | "2024-01-15T10:30:00Z" |
| category | string | News category | "politics" |
| tags | list | Topic tags | ["election", "policy"] |

## Processed Features

### linguistic_features

| Feature | Type | Description |
|---------|------|-------------|
| flesch_reading_ease | float | Flesch Reading Ease score (0-100) |
| flesch_kincaid_grade | float | Flesch-Kincaid Grade Level |
| gunning_fog | float | Gunning Fog Index |
| lexical_diversity | float | Type-Token Ratio |
| avg_sentence_length | float | Average words per sentence |
| punctuation_ratio | float | Punctuation marks / total chars |
| capitalization_ratio | float | Uppercase chars / total chars |

### sentiment_features

| Feature | Type | Description |
|---------|------|-------------|
| sentiment_neg | float | Negative sentiment score (0-1) |
| sentiment_neu | float | Neutral sentiment score (0-1) |
| sentiment_pos | float | Positive sentiment score (0-1) |
| sentiment_compound | float | Compound VADER score (-1 to 1) |
| sentiment_intensity | float | Absolute compound score |

## Labels

| Value | Meaning |
|-------|---------|
| 0 | REAL (authentic news) |
| 1 | FAKE (misinformation) |
