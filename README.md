# WarTracker 🌍

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/humac/WarTracker)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-in%20development-yellow.svg)](https://github.com/humac/WarTracker)

> Real-time global conflict tracking and analysis platform

## Mission

WarTracker provides real-time, verified information on global conflicts by continuously monitoring multiple data sources, cross-referencing reports to combat misinformation, and delivering actionable intelligence through an interactive map and customizable alerts.

## Features

### MVP (v1.0)

- ✅ **Interactive Map** - Real-time conflict visualization with severity indicators
- ✅ **Multi-Source Verification** - Cross-reference events from GDELT, ACLED, NewsAPI, UN OCHA
- ✅ **Confidence Scoring** - AI-powered verification pipeline
- ✅ **Alert System** - Customizable notifications by region and severity
- ✅ **User Authentication** - JWT + OAuth (Google, GitHub)
- ✅ **Data Export** - CSV, JSON, RSS feeds
- ✅ **Dark Mode** - Accessible UI with theme toggle

### Coming Soon

- [ ] Advanced analytics and trend detection
- [ ] Mobile applications (iOS/Android)
- [ ] Premium API tier with higher rate limits
- [ ] Satellite imagery integration
- [ ] Multi-language support

## Tech Stack

### Backend
- **FastAPI** - High-performance Python API
- **PostgreSQL + PostGIS** - Geospatial database
- **Redis** - Caching and real-time updates
- **Celery** - Async task processing
- **Ollama** - AI/ML processing (summarization, classification)

### Frontend
- **Next.js 16** - React framework with App Router
- **TypeScript** - Type-safe development
- **MapLibre GL** - Open-source interactive maps
- **Tailwind CSS** - Utility-first styling
- **Zustand** - State management

### Infrastructure
- **Docker** - Containerization
- **GitHub Actions** - CI/CD
- **Ollama Cloud** - AI models (no local GPU required)

## Quick Start

### Prerequisites

- **Docker & Docker Compose** (required for PostgreSQL + PostGIS)
- Node.js 20+ (for local frontend development)
- Python 3.11+ (for local backend development)

**Important:** WarTracker requires **PostgreSQL with PostGIS** extension for geospatial queries. The easiest way to set this up is using Docker Compose (included in this repo).

### Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/humac/WarTracker.git
   cd WarTracker
   ```

2. **Start database services (PostgreSQL + PostGIS + Redis)**
   ```bash
   docker compose up -d postgres redis
   ```
   
   Wait ~10 seconds for PostgreSQL to initialize.

3. **Enable PostGIS extension**
   ```bash
   docker exec wartracker-postgres psql -U postgres -d wartracker -c "CREATE EXTENSION IF NOT EXISTS postgis;"
   ```

4. **Run database migrations**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   alembic upgrade head
   ```

5. **Start backend**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Start frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

7. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Local Development (without Docker)

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```

## Project Structure

```
WarTracker/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── models/         # SQLAlchemy models
│   │   ├── services/       # Business logic
│   │   ├── collectors/     # Data source collectors
│   │   └── pipelines/      # Verification pipeline
│   ├── alembic/            # Database migrations
│   ├── tests/              # Unit tests
│   └── requirements.txt
│
├── frontend/               # Next.js frontend
│   ├── app/               # App Router pages
│   ├── components/        # React components
│   ├── hooks/             # Custom hooks
│   ├── stores/            # Zustand stores
│   └── package.json
│
├── docs/                   # Documentation
│   └── agent-workflow/    # Agent coordination docs
│
└── docker-compose.yml      # Docker orchestration
```

## API Documentation

Once running, visit http://localhost:8000/docs for interactive API documentation.

### Key Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/events` | GET | List conflict events |
| `/api/v1/events/{id}` | GET | Get event details |
| `/api/v1/alerts` | GET/POST | Manage user alerts |
| `/api/v1/auth/login` | POST | User authentication |
| `/api/v1/export/csv` | GET | Export data as CSV |

## Data Sources

WarTracker aggregates data from multiple sources:

| Source | Type | Credibility Tier |
|--------|------|------------------|
| GDELT Project | API | Tier 1 (Highest) |
| ACLED | API | Tier 1 (Highest) |
| UN OCHA ReliefWeb | RSS/API | Tier 1 (Highest) |
| NewsAPI | API | Tier 2 (High) |
| US State Department | RSS | Tier 1 (Highest) |

## Verification System

Events are verified through a multi-stage pipeline:

1. **Collection** - Async data ingestion from all sources
2. **Normalization** - Convert to unified schema
3. **Deduplication** - Fuzzy matching to identify duplicates
4. **Correlation** - Cross-source event matching
5. **Scoring** - Confidence calculation based on source diversity and credibility
6. **AI Processing** - Classification and summarization via Ollama

### Confidence Score Formula

```
confidence = (
    0.4 × source_diversity_score +
    0.3 × source_credibility_score +
    0.3 × detail_agreement_score
)
```

### Verification Status

| Status | Requirements | Badge |
|--------|--------------|-------|
| Verified | ≥3 sources, confidence ≥0.8 | ✓ Verified |
| Developing | 2 sources, confidence ≥0.5 | ⚡ Developing |
| Unverified | <2 sources or confidence <0.5 | ⚠ Unverified |

## Testing

### Backend Tests

```bash
cd backend
pytest --cov=app
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Security

- JWT authentication with RS256 signing
- Rate limiting (100 req/hour free tier)
- Input validation with Pydantic
- CORS protection
- SQL injection prevention (SQLAlchemy ORM)
- XSS prevention (React escaping)

## Ethical Safeguards

### Coordinate Blurring

For active high-severity conflicts, coordinates are blurred to protect civilians and aid workers:

- **Severity 1-2**: No blurring (100m precision)
- **Severity 3**: City-level (5km precision)
- **Severity 4-5**: Regional (50km precision)
- **Active conflicts**: Additional 24-hour delay

### Neutrality

WarTracker maintains strict political neutrality:
- No editorial positions
- Transparent methodology
- Multi-source verification
- Clear uncertainty indicators

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- GDELT Project for global event data
- ACLED for conflict event data
- UN OCHA for humanitarian reports
- MapLibre for open-source mapping

## Contact

- **GitHub**: https://github.com/humac/WarTracker
- **Issues**: https://github.com/humac/WarTracker/issues

---

**Disclaimer**: WarTracker provides data for informational purposes only. Data accuracy is not guaranteed. Always verify critical information from multiple sources.
