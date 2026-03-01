# WarTracker - Gemini Quick Start

## What is WarTracker?

WarTracker is a real-time global conflict tracking platform that aggregates data from multiple sources (GDELT, ACLED, NewsAPI, UN OCHA), verifies events through cross-referencing, and displays them on an interactive map.

**Quick Links:**
- **Repo:** `/home/openclaw/.openclaw/workspace/jarvis/projects/WarTracker/`
- **GitHub:** https://github.com/humac/WarTracker
- **Architecture:** `docs/agent-workflow/ARCH.md`
- **Tasks:** `docs/agent-workflow/TASKS.md`

## One-Command Setup

```bash
cd /home/openclaw/.openclaw/workspace/jarvis/projects/WarTracker
docker-compose up -d
```

Then visit:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Project Structure (TL;DR)

```
WarTracker/
├── backend/              # Python FastAPI
│   ├── app/main.py      # Entry point
│   ├── app/models/      # Database models
│   └── alembic/         # Migrations
├── frontend/            # Next.js 16
│   ├── app/page.tsx    # Homepage
│   └── components/      # React components
└── docker-compose.yml   # All services
```

## Key Commands

### Backend
```bash
cd backend
uvicorn app.main:app --reload          # Run dev server
pytest                                 # Run tests
alembic upgrade head                   # Run migrations
python scripts/seed_data.py            # Seed data
```

### Frontend
```bash
cd frontend
npm run dev                            # Run dev server
npm run build                          # Production build
npm test                               # Run tests
```

### Docker
```bash
docker-compose up                      # Start all services
docker-compose down                    # Stop all services
docker-compose logs -f backend         # View backend logs
```

## Database Schema (8 Tables)

1. **conflict_events** - Main events with location (PostGIS)
2. **sources** - Data source metadata
3. **verifications** - Event-source links
4. **users** - User accounts
5. **alerts** - User notifications
6. **regions** - Geographic areas
7. **bookmarks** - Saved events
8. **user_preferences** - User settings

## API Quick Reference

```bash
# Health check
curl http://localhost:8000/health

# List events (with filters)
curl "http://localhost:8000/api/v1/events?severity_min=3&limit=10"

# Get event details
curl http://localhost:8000/api/v1/events/1

# List regions
curl http://localhost:8000/api/v1/regions
```

## Frontend Components

### Map Component (MapLibre)
```tsx
import Map from 'react-map-gl/maplibre';

<Map
  initialViewState={{ latitude: 20, longitude: 0, zoom: 2 }}
  style={{ width: '100%', height: '100%' }}
  mapStyle="https://demotiles.maplibre.org/style.json"
>
  {/* Add markers here */}
</Map>
```

### Event Card
```tsx
<div className="bg-white dark:bg-gray-800 rounded-lg shadow p-4">
  <h3 className="font-bold">{event.title}</h3>
  <p className="text-sm text-gray-600">{event.description}</p>
  <span className={`severity-${event.severity_score}`}>
    Severity {event.severity_score}
  </span>
</div>
```

## Verification System

Events are verified through multi-source correlation:

| Status | Sources Required | Confidence |
|--------|-----------------|------------|
| ✓ Verified | ≥3 | ≥0.8 |
| ⚡ Developing | 2 | ≥0.5 |
| ⚠ Unverified | <2 | <0.5 |

## Severity Levels

- **1 (Green)**: Low impact
- **2 (Yellow)**: Moderate
- **3 (Orange)**: Serious
- **4 (Red)**: High
- **5 (Dark Red)**: Critical

## Common Tasks

### Add New Data Source
1. Add to `backend/data/sources.json`
2. Create collector in `backend/app/collectors/`
3. Run seed script

### Add New API Endpoint
1. Create router in `backend/app/api/v1/`
2. Add to `backend/app/main.py`
3. Test at `/docs`

### Add New Frontend Page
1. Create `frontend/app/your-page/page.tsx`
2. Add navigation link
3. Test at `localhost:3000/your-page`

## Testing

### Backend (pytest)
```bash
cd backend
pytest tests/test_main.py -v
pytest tests/test_models.py -v
```

### Frontend (Jest)
```bash
cd frontend
npm test -- --watchAll=false
```

## Troubleshooting

### Backend won't start
```bash
# Check database connection
docker-compose ps
# View logs
docker-compose logs backend
```

### Frontend shows blank page
```bash
# Check for build errors
npm run build
# Check console for errors
```

### Database errors
```bash
# Reset database (WARNING: deletes all data)
docker-compose down -v
docker-compose up -d postgres
alembic upgrade head
python scripts/seed_data.py
```

## Environment Setup

### Backend (.env)
```bash
DATABASE_URL=postgresql://postgres:wartracker_password_change_in_production@postgres/wartracker
REDIS_URL=redis://redis:6379
SECRET_KEY=change-in-production
```

### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Deployment Checklist

- [ ] All tests passing
- [ ] Build succeeds (`npm run build`, `pytest`)
- [ ] Database migrations applied
- [ ] Environment variables set
- [ ] Docker containers healthy
- [ ] API docs accessible
- [ ] Frontend renders correctly

## Help & Documentation

- **Full Architecture:** `docs/agent-workflow/ARCH.md`
- **Implementation Tasks:** `docs/agent-workflow/TASKS.md`
- **Requirements:** `docs/agent-workflow/REQ.md`
- **Claude Instructions:** `docs/agent-workflow/CLAUDE.md`

---

**Quick Tip:** When in doubt, check `/docs` endpoint on the backend for interactive API documentation!

**Last Updated:** 2026-03-01
