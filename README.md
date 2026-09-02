# TruthLens — Free AI-Powered Misinformation & Fact-Checking Platform

> **Before you believe it. Before you share it. Check it.**

[![Tests](https://github.com/musanyaks/fake-news-intelligence-platform/actions/workflows/tests.yml/badge.svg)](https://github.com/musanyaks/fake-news-intelligence-platform/actions/workflows/tests.yml)
[![Build](https://github.com/musanyaks/fake-news-intelligence-platform/actions/workflows/build.yml/badge.svg)](https://github.com/musanyaks/fake-news-intelligence-platform/actions/workflows/build.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

TruthLens is a **free, privacy-first AI platform** that helps people verify suspicious news, social-media claims, forwarded messages, and online information using machine learning and real-world evidence.

Built for **consumers first**, starting with **Kenya and East Africa**.

---

## Free Forever

| Feature | Cost |
|---------|------|
| Check text / URL / headline | Free |
| Paste WhatsApp messages | Free |
| Source analysis | Free |
| Fact-check search | Free |
| Evidence links | Free |
| Browser extension | Free |
| Account required | No |
| Credit card | No |

---

## What Makes TruthLens Different

### Kenya-First
Designed to handle misinformation relevant to Kenya and Africa, with local source registries and fact-check partners.

### Evidence-First
AI does not simply say "fake"; it shows **why** — with sources, fact-checks, and confidence scores.

### Privacy-First
We do not build a database of people's private messages. Checks are ephemeral by default.

### Consumer-First
Core verification remains free. Institutional APIs and dashboards are optional paid tiers.

---

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+ (for frontend)
- Docker & Docker Compose (optional)

### Backend

```bash
cd truthlens
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
pip install -e ".[dev]"
make api
```

API docs: http://localhost:8000/docs

### Frontend

```bash
cd frontend/web
npm install
npm run dev
```

Open: http://localhost:3000

### Full Stack (Docker)

```bash
docker-compose up -d
```

---

## The Verdict System

TruthLens does not simply return "FAKE". We use a nuanced, evidence-based verdict system:

| Verdict | Color | Meaning |
|---------|-------|---------|
| **Supported** | Green | Evidence supports the claim |
| **Unverified** | Yellow | Not enough reliable evidence |
| **Misleading** | Orange | Some truth, but presentation is misleading |
| **Likely False** | Red | Reliable evidence contradicts the claim |
| **Opinion** | Blue | Primarily an opinion, not a factual claim |
| **Satire** | Purple | Likely intended as satire / parody |

---

## Architecture

```
Consumers
    |
    +-- Web App (Next.js)
    +-- Browser Extension
    +-- Mobile PWA
    |
    v
FastAPI Gateway
    |
    +-- Claim Extraction
    +-- URL Processing
    +-- Image OCR
    |
    v
Verification Engine
    |
    +-- RoBERTa / NLP Scoring
    +-- Fact-Check Search (Google Fact Check, Africa Check, PesaCheck)
    +-- Source Credibility Analysis
    +-- Web Evidence Retrieval
    |
    v
Evidence Fusion
    |
    v
Truth Score + Consumer Result
```

Behind the consumer layer, TruthLens runs a full MLOps stack:

```
Kafka -> Spark -> Feature Engineering -> Model Training (MLflow)
-> Model Registry -> FastAPI -> Prometheus / Grafana / Evidently
-> Airflow (retraining, monitoring, ingestion)
```

---

## Project Structure

```
truthlens/
├── frontend/
│   ├── web/              # Next.js consumer app
│   └── extension/        # Browser extension
├── api/                  # FastAPI backend
│   ├── routes/
│   │   ├── verification.py   # Main consumer endpoint
│   │   ├── evidence.py
│   │   ├── claims.py
│   │   ├── prediction.py
│   │   └── health.py
│   └── schemas/
├── src/
│   ├── claim_extraction/     # Extract claims from text/URL/image
│   ├── evidence/             # Fact-check, search, source analysis
│   ├── source_credibility/   # Source registry & scoring
│   ├── verification/         # Evidence fusion engine
│   ├── scoring/              # Truth score calculation
│   ├── ingestion/
│   ├── preprocessing/
│   ├── features/
│   ├── models/
│   ├── explainability/
│   └── utils/
├── training/
├── airflow/                  # DAGs for ingestion, training, monitoring
├── database/
├── monitoring/               # Prometheus, Grafana, Evidently
├── deployment/               # Docker, K8s, Terraform, Helm
├── tests/
└── docs/
    ├── architecture/
    ├── api/
    ├── model-card/
    ├── privacy/
    └── consumer-guide/
```

---

## Development Phases

| Phase | Feature |
|-------|---------|
| 1 | Consumer web app + /verify endpoint + result page |
| 2 | URL extraction + article parsing |
| 3 | Evidence engine (fact-checks, sources, web search) |
| 4 | Kenya-specific source registry |
| 5 | Screenshot / image OCR checker |
| 6 | Browser extension |
| 7 | WhatsApp / social workflow |
| 8 | Kafka + Spark production ingestion |
| 9 | Monitoring + automated retraining |
| 10 | Cloud deployment |

---

## API Usage

### Verify a Claim

```bash
curl -X POST "http://localhost:8000/api/v1/verify" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Kenya has banned all mobile money withdrawals above KSh 50,000",
    "type": "text"
  }'
```

**Response:**
```json
{
  "verdict": "Likely Misleading",
  "verdict_color": "orange",
  "confidence": 0.86,
  "evidence_score": 78,
  "source_agreement": 82,
  "fact_check_matches": 3,
  "explanation": "The claim does not match available evidence from CBK.",
  "recommendation": "Don't share until verified.",
  "sources": [...],
  "fact_checks": [...],
  "share_url": "https://truthlens.example/check/abc123"
}
```

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Open a Pull Request

---

## License

MIT License — see [LICENSE](LICENSE) file.

## Acknowledgments

- HuggingFace Transformers
- Africa Check, PesaCheck, and other fact-checking organizations
- The open-source MLOps community
