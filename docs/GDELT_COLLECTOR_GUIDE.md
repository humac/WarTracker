# GDELT Collector Guide

## Overview

The GDELT Collector is WarTracker's primary data ingestion pipeline for global conflict events. It fetches real-time news and event data from the GDELT Project (FREE, no API key required) and stores it in a PostGIS-enabled PostgreSQL database.

**Key Features:**
- ✅ No API key required
- ✅ Real-time data collection
- ✅ Automatic event classification
- ✅ Severity scoring
- ✅ Geolocation via country centroids
- ✅ Comprehensive error handling
- ✅ Retry logic (3 attempts)

---

## Quick Start

### Prerequisites

1. **PostgreSQL with PostGIS** running via Docker:
   ```bash
   docker compose up -d postgres
   ```

2. **PostGIS extension** enabled:
   ```bash
   docker exec wartracker-postgres psql -U postgres -d wartracker -c "CREATE EXTENSION IF NOT EXISTS postgis;"
   ```

3. **Python virtual environment** activated:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or: venv\Scripts\activate  # Windows
   ```

4. **Dependencies** installed:
   ```bash
   pip install -r requirements.txt
   ```

### First Collection

**Collect 100 events and save to database:**
```bash
python scripts/collect_data.py --limit 100
```

**Expected output:**
```
Starting data collection...
Enabled sources: ['gdelt']
Collecting from: gdelt
✅ GDELT: Collected 100 events
Collection complete. Saved 100 events to database.
```

---

## CLI Usage

### Basic Commands

**Collect and save:**
```bash
python scripts/collect_data.py --limit 100
```

**Dry run (preview without saving):**
```bash
python scripts/collect_data.py --dry-run --limit 5
```

**Collect from specific sources:**
```bash
python scripts/collect_data.py --sources gdelt --limit 50
```

**Show help:**
```bash
python scripts/collect_data.py --help
```

### CLI Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--sources` | str | All enabled | Comma-separated list of sources (e.g., `gdelt,acled`) |
| `--limit` | int | 100 | Maximum records to collect per source |
| `--dry-run` | flag | False | Collect data but don't save to database |
| `--help` | flag | - | Show help message and exit |

### Examples

**Test collection (5 events, no save):**
```bash
python scripts/collect_data.py --dry-run --limit 5
```

**Collect from GDELT only (200 events):**
```bash
python scripts/collect_data.py --sources gdelt --limit 200
```

**Collect from multiple sources:**
```bash
python scripts/collect_data.py --sources gdelt,acled --limit 100
```

**Large collection (500 events):**
```bash
python scripts/collect_data.py --limit 500
```

---

## API Access

Once data is collected, query it via the REST API.

### Get All Events

```bash
curl http://localhost:8000/api/v1/events
```

**Response:**
```json
{
  "events": [
    {
      "id": 1,
      "title": "Protests escalate in capital city",
      "event_type": "protest",
      "severity_score": 3,
      "latitude": 40.7128,
      "longitude": -74.0060,
      "timestamp": "2026-03-02T01:00:00Z",
      "sources": ["gdelt"],
      "confidence_score": 0.5
    }
  ],
  "total": 100
}
```

### Filter by Severity

```bash
curl "http://localhost:8000/api/v1/events?severity_min=4"
```

### Filter by Date Range

```bash
curl "http://localhost:8000/api/v1/events?start_date=2026-03-01&end_date=2026-03-02"
```

### Pagination

```bash
curl "http://localhost:8000/api/v1/events?skip=0&limit=50"
```

### API Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `severity_min` | int | 1 | Minimum severity (1-5) |
| `severity_max` | int | 5 | Maximum severity (1-5) |
| `event_type` | str | All | Filter by event type |
| `start_date` | date | 30 days ago | Start of date range |
| `end_date` | date | Today | End of date range |
| `skip` | int | 0 | Pagination offset |
| `limit` | int | 100 | Max results (1-1000) |

---

## Event Classification

The GDELT collector automatically classifies events into categories:

| Event Type | Keywords | Severity |
|------------|----------|----------|
| **battle** | battle, clash, fighting, offensive | 4 |
| **attack** | attack, bomb, explosion, shooting | 5 |
| **military_action** | military, army, forces, deployment | 3 |
| **riot** | riot, unrest, disturbance | 3 |
| **protest** | protest, demonstration, rally | 2 |
| **conflict** | conflict, crisis, tension | 3 |
| **other** | (default) | 2 |

**Classification Logic:**
1. Scan title and description for keywords
2. Match against event type patterns (case-insensitive)
3. Assign severity based on event type
4. Default to "other" if no match

---

## Geolocation

### How It Works

GDELT v2/doc API doesn't provide precise coordinates. The collector uses **country centroids** as an approximation:

1. Extract country name from article
2. Look up country centroid (lat/lon)
3. Store as PostGIS POINT geometry

### Country Coverage

The collector includes centroids for 50+ countries:
- Ukraine: (48.3794, 31.1656)
- Russia: (61.5240, 105.3188)
- Israel: (31.0461, 34.8516)
- Palestine: (31.9522, 35.2332)
- Syria: (34.8021, 38.9968)
- Yemen: (15.5527, 48.5164)
- ...and 44 more

### Limitations

- **Precision:** Country-level only (not city-specific)
- **Large countries:** Centroid may be far from actual event (e.g., Mexico, Russia)
- **Future improvement:** Use GDELT GKG or Event API for precise coordinates

---

## Database Schema

### ConflictEvent Table

```sql
CREATE TABLE conflict_events (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    event_type VARCHAR(50) NOT NULL,
    severity_score INTEGER NOT NULL,
    location GEOMETRY(POINT, 4326) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    sources TEXT[] NOT NULL,
    confidence_score FLOAT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Spatial index for fast location queries
CREATE INDEX idx_events_location ON conflict_events USING GIST (location);

-- Temporal index for date range queries
CREATE INDEX idx_events_timestamp ON conflict_events (timestamp DESC);

-- Text search index
CREATE INDEX idx_events_title ON conflict_events USING GIN (to_tsvector('english', title));
```

### Query Examples

**Events near a location (50km radius):**
```sql
SELECT * FROM conflict_events
WHERE ST_DWithin(
    location,
    ST_MakePoint(-74.0060, 40.7128)::geography,
    50000
);
```

**Events by date range:**
```sql
SELECT * FROM conflict_events
WHERE timestamp BETWEEN '2026-03-01' AND '2026-03-02';
```

**High-severity events:**
```sql
SELECT * FROM conflict_events
WHERE severity_score >= 4
ORDER BY timestamp DESC;
```

---

## Scheduling Production Collection

### Cron Job (Linux/Mac)

**Edit crontab:**
```bash
crontab -e
```

**Add daily collection at 6 AM UTC:**
```bash
0 6 * * * cd /path/to/WarTracker/backend && source venv/bin/activate && python scripts/collect_data.py --limit 500 >> /var/log/wartracker-collection.log 2>&1
```

**Add hourly collection:**
```bash
0 * * * * cd /path/to/WarTracker/backend && source venv/bin/activate && python scripts/collect_data.py --limit 100 >> /var/log/wartracker-collection.log 2>&1
```

### Systemd Timer (Linux)

**Create service file** (`/etc/systemd/system/wartracker-collector.service`):
```ini
[Unit]
Description=WarTracker Data Collection
After=network.target

[Service]
Type=oneshot
User=wartracker
WorkingDirectory=/path/to/WarTracker/backend
Environment=PATH=/path/to/WarTracker/backend/venv/bin
ExecStart=python scripts/collect_data.py --limit 500
```

**Create timer file** (`/etc/systemd/system/wartracker-collector.timer`):
```ini
[Unit]
Description=Run WarTracker collection daily
Requires=wartracker-collector.service

[Timer]
OnCalendar=*-*-* 06:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

**Enable and start:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable wartracker-collector.timer
sudo systemctl start wartracker-collector.timer
```

**Check status:**
```bash
sudo systemctl list-timers
sudo systemctl status wartracker-collector.timer
```

### Windows Task Scheduler

**PowerShell script** (`collect_daily.ps1`):
```powershell
cd C:\path\to\WarTracker\backend
.\venv\Scripts\Activate.ps1
python scripts\collect_data.py --limit 500
```

**Schedule via Task Scheduler:**
1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Daily at 6:00 AM
4. Action: Start a program
   - Program: `powershell.exe`
   - Arguments: `-ExecutionPolicy Bypass -File C:\path\to\collect_daily.ps1`

---

## Monitoring & Logging

### Check Collection Logs

```bash
tail -f /var/log/wartracker-collection.log
```

### Verify Data in Database

```bash
docker exec -it wartracker-postgres psql -U postgres -d wartracker -c "SELECT COUNT(*) FROM conflict_events;"
```

### Check Latest Events

```bash
docker exec -it wartracker-postgres psql -U postgres -d wartracker -c "SELECT title, event_type, severity_score, timestamp FROM conflict_events ORDER BY timestamp DESC LIMIT 10;"
```

### API Health Check

```bash
curl http://localhost:8000/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "sources_enabled": ["gdelt"]
}
```

---

## Troubleshooting

### Issue: "Connection refused" to database

**Solution:**
```bash
docker compose up -d postgres
# Wait 10 seconds
docker exec wartracker-postgres psql -U postgres -d wartracker -c "CREATE EXTENSION IF NOT EXISTS postgis;"
```

### Issue: "PostGIS extension not found"

**Solution:**
```bash
docker exec wartracker-postgres psql -U postgres -d wartracker -c "CREATE EXTENSION postgis;"
```

### Issue: No events collected

**Possible causes:**
1. GDELT API temporarily unavailable
2. Network connectivity issue
3. Rate limiting

**Solution:**
- Check logs for error messages
- Retry with `--dry-run` to test
- Wait 5 minutes and try again

### Issue: Invalid coordinates

**Symptoms:** Events have lat/lon of (0, 0) or NULL

**Solution:**
- Check country name extraction in logs
- Verify country is in centroid lookup table
- Add missing country to `COUNTRY_CENTROIDS` in `gdelt.py`

### Issue: Duplicate events

**Solution:**
- Run deduplication script (future feature)
- Manually remove duplicates via SQL:
  ```sql
  DELETE FROM conflict_events a USING conflict_events b
  WHERE a.id < b.id
    AND a.title = b.title
    AND a.timestamp = b.timestamp;
  ```

---

## Adding New Data Sources

### Step 1: Create Collector Class

Create `backend/app/collectors/newsource.py`:

```python
from typing import List, Dict, Any
from .base import BaseCollector

class NewSourceCollector(BaseCollector):
    name = "newsource"
    requires_api_key = True  # or False
    
    def __init__(self, api_key: str = None):
        super().__init__()
        self.api_key = api_key
        self.base_url = "https://api.newsource.com/v1"
    
    async def fetch(self) -> List[Dict[str, Any]]:
        """Fetch raw data from source API."""
        # Implement API call
        pass
    
    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize to WarTracker schema."""
        # Implement normalization
        pass
```

### Step 2: Register Collector

Edit `backend/app/collectors/manager.py`:

```python
from .newsource import NewSourceCollector

class CollectorManager:
    def __init__(self):
        self.collectors = {
            "gdelt": GDELTCollector(),
            "newsource": NewSourceCollector(api_key=self.config.NEWSOURCE_API_KEY),
        }
```

### Step 3: Add Configuration

Edit `backend/app/config.py`:

```python
class Settings(BaseSettings):
    # ... existing config ...
    NEWSOURCE_API_KEY: Optional[str] = None
```

### Step 4: Add Tests

Create `backend/tests/test_newsource.py`:

```python
import pytest
from app.collectors.newsource import NewSourceCollector

class TestNewSourceCollector:
    def test_collector_initialization(self):
        collector = NewSourceCollector()
        assert collector.name == "newsource"
    
    # Add more tests...
```

### Step 5: Update Documentation

- Add to `README.md` data sources table
- Add usage examples to this guide
- Update `docs/RUN_STATE.md`

---

## Best Practices

### Collection Frequency

| Use Case | Frequency | Limit |
|----------|-----------|-------|
| Development/Testing | On-demand | 5-10 events |
| Production (MVP) | Daily | 100-500 events |
| Production (Full) | Hourly | 50-100 events/hour |
| High-priority crisis | Every 15 min | 25 events/collection |

### Rate Limiting

- GDELT: No official rate limit (be respectful)
- Recommended: Max 100 requests/hour
- Implement exponential backoff on errors

### Data Quality

- **Validate** all events before saving
- **Log** collection statistics (events collected, saved, errors)
- **Monitor** data freshness (time since last collection)
- **Alert** on collection failures

### Performance

- Use `--limit` to control collection size
- Run collection during off-peak hours
- Consider async collection for multiple sources
- Cache API responses (Redis, 15-min TTL)

---

## Security

### API Keys

- Store in environment variables (`.env` file)
- Never commit `.env` to git
- Use `.env.example` as template
- Rotate keys periodically

### Database Access

- Use read-only credentials for API endpoints
- Use write credentials only for collection script
- Enable SSL for production database connections

### Rate Limiting

- API endpoints: 100 req/min (default)
- Adjust based on deployment needs
- Monitor for abuse patterns

---

## Future Enhancements

### Planned Features

1. **ACLED Integration** - High-quality conflict data (API key required)
2. **NewsAPI Integration** - Broader news coverage (API key required)
3. **UN OCHA ReliefWeb** - Humanitarian crisis reports (RSS feed)
4. **AI Classification** - Ollama-powered event categorization
5. **Multi-source Verification** - Cross-reference events across sources
6. **Deduplication** - Fuzzy matching to identify duplicate events
7. **Real-time Streaming** - WebSocket updates for new events

### Roadmap

- **Q2 2026:** ACLED + NewsAPI integration
- **Q3 2026:** AI classification pipeline
- **Q4 2026:** Multi-source verification system

---

## Support

### Documentation

- **Main README:** `/home/openclaw/.openclaw/workspace/jarvis/projects/WarTracker/README.md`
- **Implementation Report:** `docs/GDELT_IMPLEMENTATION_REPORT.md`
- **Ownership Report:** `docs/GDELT_COLLECTOR_OWNERSHIP.md`
- **QA Report:** `docs/agent-workflow/QA.md`

### Contact

- **GitHub Issues:** https://github.com/humac/WarTracker/issues
- **Owner:** Peter (Developer)

---

**Last Updated:** 2026-03-02  
**Version:** 1.0.0  
**Status:** Production Ready ✅
