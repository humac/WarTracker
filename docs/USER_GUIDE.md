# WarTracker User Guide

## Getting Started

### Prerequisites
- Docker & Docker Compose
- Python 3.10+
- Node.js 18+

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/humac/WarTracker.git
   cd WarTracker
   ```

2. **Set up environment variables:**
   ```bash
   cp backend/.env.example backend/.env
   # Edit backend/.env with your API keys (GDELT, ACLED, NewsAPI)
   ```

3. **Start services:**
   ```bash
   docker-compose up -d
   ```

4. **Run backend:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   alembic upgrade head
   uvicorn app.main:app --reload
   ```

5. **Run frontend:**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

6. **Open http://localhost:3000**

---

## Features

### Real-Time Conflict Map
- View conflict events on interactive map
- Color-coded by severity (green=low, yellow=medium, orange=high, red=critical)
- Click markers for event details, sources, and timeline
- Filter by severity, event type, date range, and region

### Multi-Source Verification
- Aggregates data from GDELT, ACLED, NewsAPI, UN OCHA, and government sources
- Confidence scoring (0.0-1.0) based on source diversity and credibility
- Multi-source correlation with verification badges:
  - ✓ **Verified** - 3+ sources, confidence ≥0.8
  - ⚡ **Developing** - 2 sources, confidence ≥0.5
  - ⚠ **Unverified** - <2 sources or confidence <0.5

### Alerts
- Set up custom alerts by region, conflict type, and severity threshold
- Real-time push notifications for high-severity events
- Email/webhook notifications (configurable frequency)
- Alert management dashboard (create, edit, pause, delete)

### Data Export
- Export filtered events as CSV or JSON
- RSS feeds for custom alerts
- API access for programmatic usage (100 req/hour free tier)

---

## API Reference

### Base URL
```
http://localhost:8000/api/v1
```

### Authentication Endpoints

#### POST /auth/register
Register a new user account.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "username": "username"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### POST /auth/login
Login with email and password.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

### Conflict Event Endpoints

#### GET /events
List conflict events with filters.

**Query Parameters:**
- `lat`, `lng`, `radius` - Geospatial filter (radius in km)
- `severity_min`, `severity_max` - Filter by severity (1-5)
- `event_type` - Filter by type (armed_conflict, protest, terrorism, etc.)
- `date_from`, `date_to` - Date range (ISO 8601 format)
- `country` - Country code filter (e.g., "SY", "UA")
- `verified` - Filter by verification status (true/false)
- `limit`, `offset` - Pagination (default: 50, max: 500)

**Example:**
```bash
curl "http://localhost:8000/api/v1/events?lat=33.88&lng=35.50&radius=50&severity_min=4&limit=20"
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 12345,
      "title": "Armed clash in northern Syria",
      "event_type": "armed_conflict",
      "severity_score": 4,
      "location": {
        "lat": 33.88,
        "lng": 35.50
      },
      "event_timestamp": "2026-03-01T14:30:00Z",
      "verification_status": "verified",
      "confidence_score": 0.85,
      "source_count": 3,
      "casualties_min": 5,
      "casualties_max": 12
    }
  ],
  "meta": {
    "total": 156,
    "page": 1,
    "per_page": 20
  }
}
```

#### GET /events/{id}
Get details for a specific event.

**Example:**
```bash
curl http://localhost:8000/api/v1/events/12345
```

#### GET /events/stats
Get aggregate statistics.

**Response:**
```json
{
  "total_active": 156,
  "last_24h": 23,
  "by_severity": {
    "1": 45,
    "2": 38,
    "3": 42,
    "4": 21,
    "5": 10
  },
  "by_region": {
    "Middle East": 67,
    "Eastern Europe": 34,
    "Africa": 28,
    "Asia": 27
  }
}
```

### Source Endpoints

#### GET /sources
List all data sources with status.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "GDELT Project",
      "source_type": "api",
      "credibility_tier": 1,
      "credibility_score": 0.95,
      "is_active": true,
      "last_checked": "2026-03-01T23:00:00Z",
      "total_reports": 4523,
      "verified_reports": 3891
    }
  ]
}
```

### Alert Endpoints (Authenticated)

#### GET /alerts
List user's alerts.

**Headers:**
```
Authorization: Bearer <access_token>
```

#### POST /alerts
Create a new alert.

**Request:**
```json
{
  "name": "Syria High Severity",
  "region_filter": {
    "country_codes": ["SY"],
    "region_names": []
  },
  "conflict_type_filter": ["armed_conflict", "airstrike"],
  "severity_threshold": 4,
  "notification_method": "push"
}
```

---

## Troubleshooting

### Common Issues

#### Database Connection Errors
**Symptom:** Backend fails to start with "could not connect to server"

**Solution:**
1. Ensure PostgreSQL is running: `docker-compose ps`
2. Check DATABASE_URL in backend/.env
3. Verify port 5432 is not in use: `lsof -i :5432`

#### API Key Configuration
**Symptom:** Collectors fail with "authentication failed" or "invalid API key"

**Solution:**
1. Obtain API keys from:
   - GDELT: https://www.gdeltproject.org/
   - ACLED: https://www.acleddata.com/
   - NewsAPI: https://newsapi.org/
2. Update backend/.env with valid keys
3. Restart collectors: `docker-compose restart celery`

#### Port Conflicts
**Symptom:** "Address already in use" error

**Solution:**
1. Check what's using the port: `lsof -i :8000` or `lsof -i :3000`
2. Stop conflicting service or change port in configuration
3. For frontend, update frontend/.env.local: `NEXT_PUBLIC_API_URL=http://localhost:8001`

#### Frontend Shows Black Screen
**Symptom:** Page loads but shows only black screen or raw text

**Solution:**
1. Check browser console for errors (F12)
2. Verify backend is running: `curl http://localhost:8000/health`
3. Clear browser cache and reload
4. Ensure Node.js version is 18+: `node --version`

#### WebGL Not Available
**Symptom:** Map doesn't load, shows "WebGL not supported"

**Solution:**
- This is expected in headless browsers or systems without GPU
- Fallback to event list view is automatic
- For development, use a browser with WebGL support (Chrome, Firefox)

---

## Support

- **GitHub Issues:** https://github.com/humac/WarTracker/issues
- **Documentation:** https://github.com/humac/WarTracker/docs
- **API Documentation:** http://localhost:8000/docs (when running)

---

## Security Best Practices

1. **Never commit .env files** - Add to .gitignore
2. **Use strong passwords** - Minimum 12 characters, mix of types
3. **Rotate API keys regularly** - Especially if exposed
4. **Enable 2FA** - When OAuth is configured
5. **Review alert notifications** - Don't share sensitive alert configurations

---

**Version:** 1.0.0  
**Last Updated:** 2026-03-01  
**Maintained by:** WarTracker Team
