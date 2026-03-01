# WarTracker - Claude Instructions

## Project Overview

**WarTracker** is a real-time global conflict tracking platform that monitors multiple data sources (GDELT, ACLED, NewsAPI, UN OCHA), cross-references reports for verification, and displays conflicts on an interactive map with severity indicators.

**Repository:** `/home/openclaw/.openclaw/workspace/jarvis/projects/WarTracker/`  
**GitHub:** https://github.com/humac/WarTracker  
**Stack:** Next.js 16 + FastAPI + PostgreSQL + PostGIS + Redis + Ollama

## Architecture Summary

### Backend (FastAPI)
- **Location:** `backend/`
- **Entry Point:** `backend/app/main.py`
- **Database:** PostgreSQL 15 with PostGIS extension
- **Models:** SQLAlchemy ORM in `backend/app/models/`
- **Migrations:** Alembic in `backend/alembic/`
- **API:** RESTful `/api/v1/` endpoints

### Frontend (Next.js 16)
- **Location:** `frontend/`
- **Entry Point:** `frontend/app/page.tsx`
- **Styling:** Tailwind CSS
- **Map:** MapLibre GL via react-map-gl
- **State:** Zustand for client state, React Query for server state

### Infrastructure
- **Docker:** `docker-compose.yml` orchestrates all services
- **Redis:** Caching and real-time updates
- **Celery:** Async task processing for data collectors
- **Ollama:** AI/ML for summarization and classification

## Key Files

| File | Purpose |
|------|---------|
| `docker-compose.yml` | Service orchestration |
| `backend/app/main.py` | FastAPI application |
| `backend/app/models/*.py` | SQLAlchemy models (8 tables) |
| `backend/alembic/versions/` | Database migrations |
| `frontend/app/page.tsx` | Homepage |
| `frontend/app/layout.tsx` | Root layout |
| `docs/agent-workflow/ARCH.md` | Full architecture |
| `docs/agent-workflow/TASKS.md` | Implementation tasks |
| `docs/agent-workflow/REQ.md` | Requirements |

## Common Tasks

### Run Backend Tests
```bash
cd backend
pytest --cov=app
```

### Run Frontend Tests
```bash
cd frontend
npm test
```

### Start Development Servers
```bash
# Option 1: Docker (all services)
docker-compose up

# Option 2: Local backend
cd backend
uvicorn app.main:app --reload

# Option 3: Local frontend
cd frontend
npm run dev
```

### Database Migrations
```bash
cd backend
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

### Seed Initial Data
```bash
cd backend
python scripts/seed_data.py
```

## API Endpoints

### Public Endpoints
- `GET /health` - Health check
- `GET /` - Root info
- `GET /api/v1/events` - List events (with filters)
- `GET /api/v1/events/{id}` - Get event details
- `GET /api/v1/regions` - List regions
- `GET /api/v1/sources` - List sources

### Authenticated Endpoints
- `POST /api/v1/auth/register` - Register user
- `POST /api/v1/auth/login` - Login
- `GET /api/v1/alerts` - User's alerts
- `POST /api/v1/alerts` - Create alert
- `GET /api/v1/users/me` - Current user profile

## Database Schema

### Core Tables
1. **conflict_events** - Main event table with PostGIS geometry
2. **sources** - Data source metadata and credibility
3. **verifications** - Links events to sources
4. **users** - User accounts
5. **alerts** - User alert preferences
6. **regions** - Geographic regions
7. **bookmarks** - User-saved events
8. **user_preferences** - User settings

### Key Relationships
- `ConflictEvent` ←→ `Verification` ←→ `Source`
- `User` ←→ `Alert`
- `User` ←→ `Bookmark` ←→ `ConflictEvent`

## Verification Pipeline

Events go through multi-stage verification:

1. **Collection** → 2. **Normalization** → 3. **Deduplication** → 4. **Correlation** → 5. **Scoring** → 6. **AI Processing**

### Confidence Score
```python
confidence = (
    0.4 * source_diversity_score +
    0.3 * source_credibility_score +
    0.3 * detail_agreement_score
)
```

### Verification Status
- **Verified**: ≥3 sources, confidence ≥0.8
- **Developing**: 2 sources, confidence ≥0.5
- **Unverified**: <2 sources or confidence <0.5

## Severity Colors

| Level | Color | Hex |
|-------|-------|-----|
| 1 (Low) | Green | #22c55e |
| 2 (Moderate) | Yellow | #eab308 |
| 3 (Serious) | Orange | #f97316 |
| 4 (High) | Red | #ef4444 |
| 5 (Critical) | Dark Red | #7f1d1d |

## Environment Variables

### Backend (.env)
```bash
DATABASE_URL=postgresql://postgres:password@localhost/wartracker
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key
OLLAMA_API_URL=http://localhost:11434
```

### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws
```

## Testing Guidelines

1. **Backend**: Use pytest fixtures in `conftest.py`
2. **Frontend**: Use React Testing Library
3. **Coverage Target**: ≥80%
4. **Run before commit**: Always run tests before committing

## Code Style

### Backend (Python)
- Type hints required
- Pydantic models for validation
- Async/await for I/O operations
- Structlog for logging

### Frontend (TypeScript)
- Strict TypeScript
- Functional components with hooks
- Tailwind for styling
- Client components marked with `'use client'`

## Security Notes

- JWT tokens: 15-minute access, 7-day refresh
- Rate limiting: 100 req/hour (free tier)
- CORS: Configured for localhost:3000 and production domains
- Input validation: Pydantic on backend, Zod on frontend
- Coordinate blurring for active high-severity conflicts

## Common Issues & Solutions

### PostGIS Extension Not Found
```sql
CREATE EXTENSION IF NOT EXISTS postgis;
```

### MapLibre Not Rendering
- Check API key (if using styled tiles)
- Verify container has dimensions
- Check browser console for errors

### Database Connection Refused
- Ensure PostgreSQL container is running: `docker-compose ps`
- Check connection string in `.env`
- Verify port 5432 is not in use

## Handoff Checklist

Before handing off to Heimdall (QA):

- [ ] All tests passing (`pytest`, `npm test`)
- [ ] Build succeeds (`npm run build`)
- [ ] Dev server runs without errors
- [ ] Browser shows styled UI (not black screen)
- [ ] Screenshots captured in `docs/screenshots/`
- [ ] Screenshots verified (opened and confirmed correct)
- [ ] RUN_STATE.md updated
- [ ] This file updated with any new patterns

---

**Last Updated:** 2026-03-01  
**Version:** 1.0.0 (MVP in development)
