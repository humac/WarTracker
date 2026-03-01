# WarTracker - System Architecture

## Version
v1.0 (Initial Architecture)

## System Overview

WarTracker is a real-time global conflict tracking platform that continuously monitors multiple data sources, cross-references reports to combat misinformation, and delivers actionable intelligence through an interactive map and customizable alerts.

The system follows a **event-driven architecture** with async data ingestion, multi-source verification pipeline, and real-time frontend updates. The architecture prioritizes:
- **Data accuracy** through multi-source verification
- **Performance** through multi-layer caching and optimized geospatial queries
- **Scalability** through containerized, horizontally-scalable services
- **Ethical responsibility** through coordinate blurring and bias mitigation

## Architecture Diagram

```mermaid
graph TB
    subgraph Data Sources
        GDELT[GDELT API]
        ACLED[ACLED API]
        NewsAPI[NewsAPI]
        UNOCHA[UN OCHA ReliefWeb]
        Govt[Government Reports]
        Social[Social Media]
    end

    subgraph Ingestion Layer
        Collectors[Data Collectors<br/>Async Workers]
        Queue[Redis Queue<br/>Task Distribution]
        Normalizer[Data Normalizer<br/>Unified Schema]
    end

    subgraph Processing Layer
        Dedup[Deduplication Engine<br/>Fuzzy Matching]
        Verifier[Verification Pipeline<br/>Multi-Source Correlation]
        Scorer[Confidence Scorer<br/>Source Trust Weights]
        AIProc[AI Processing<br/>Summarization & Classification]
    end

    subgraph Storage Layer
        PG[(PostgreSQL + PostGIS<br/>Conflict Events & Metadata)]
        Redis[(Redis<br/>Cache & Sessions)]
    end

    subgraph API Layer
        FastAPI[FastAPI Backend<br/>RESTful API /api/v1/]
        Auth[Authentication<br/>JWT + OAuth]
        RateLimit[Rate Limiter<br/>API Protection]
    end

    subgraph Frontend
        NextJS[Next.js 16 App<br/>Interactive Map]
        WebSocket[WebSocket Client<br/>Real-time Updates]
        Components[React Components<br/>Map, Filters, Alerts]
    end

    subgraph Users
        Journalist[Journalists]
        Researcher[Researchers]
        NGO[NGO Workers]
        Public[General Public]
    end

    GDELT --> Collectors
    ACLED --> Collectors
    NewsAPI --> Collectors
    UNOCHA --> Collectors
    Govt --> Collectors
    Social --> Collectors

    Collectors --> Queue
    Queue --> Normalizer
    Normalizer --> Dedup
    Dedup --> Verifier
    Verifier --> Scorer
    Scorer --> AIProc
    AIProc --> PG

    Redis -.-> PG
    Redis -.-> FastAPI

    FastAPI --> Auth
    FastAPI --> RateLimit

    NextJS --> WebSocket
    NextJS --> Components
    WebSocket --> FastAPI
    Components --> FastAPI

    FastAPI --> NextJS
    NextJS --> Journalist
    NextJS --> Researcher
    NextJS --> NGO
    NextJS --> Public

    style Collectors fill:#e1f5ff
    style Verifier fill:#fff4e1
    style PG fill:#e8f5e9
    style NextJS fill:#f3e5f5
```

## Technology Stack

### Frontend
- **Next.js 16** (App Router) - React framework with server-side rendering
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **MapLibre GL** - Open-source vector map library (no licensing costs)
- **Zustand** - Lightweight state management (simpler than Redux, sufficient for our needs)
- **React Query** - Server state management and caching
- **Socket.io Client** - Real-time WebSocket communication

### Backend
- **FastAPI** (Python 3.11+) - High-performance async API framework
- **PostgreSQL 15** - Primary database with ACID compliance
- **PostGIS** - Geospatial extensions for location-based queries
- **Redis 7** - Caching, session storage, and task queues
- **Celery** - Async task queue for data collectors
- **Pydantic** - Data validation and settings management

### Infrastructure
- **Docker** - Containerization for consistent deployment
- **Docker Compose** - Local development orchestration
- **Kubernetes** (optional for production) - Container orchestration
- **Nginx** - Reverse proxy and static file serving
- **Let's Encrypt** - SSL/TLS certificates
- **GitHub Actions** - CI/CD pipeline

### AI/ML
- **Ollama Cloud** - All AI/ML processing (no local GPU required)
  - Text summarization
  - Conflict classification
  - Trend analysis
  - Misinformation detection

### Monitoring & Observability
- **Prometheus** - Metrics collection
- **Grafana** - Visualization and dashboards
- **ELK Stack** (Elasticsearch, Logstash, Kibana) - Log aggregation
- **Sentry** - Error tracking

## Database Schema

### ERD

```mermaid
erDiagram
    conflict_events ||--o{ verifications : "has"
    conflict_events ||--o{ sources : "reported_by"
    conflict_events ||--o{ alerts : "triggers"
    conflict_events }o--|| regions : "located_in"
    users ||--o{ alerts : "creates"
    users ||--o{ bookmarks : "creates"
    users ||--o{ user_preferences : "has"
    sources ||--o{ verifications : "verified_by"

    conflict_events {
        bigint id PK
        geometry location "PostGIS POINT"
        varchar event_type
        varchar title
        text description
        integer severity_score "1-5"
        integer casualties_min
        integer casualties_max
        timestamp event_timestamp
        timestamp created_at
        timestamp updated_at
        varchar verification_status "unverified|verified|disputed"
        float confidence_score "0.0-1.0"
        boolean is_active
        varchar actors_involved "JSON array"
        varchar country_code
        varchar region_name
    }

    sources {
        bigint id PK
        varchar name
        varchar url
        varchar source_type "api|rss|manual|social"
        integer credibility_tier "1-4"
        float credibility_score "0.0-1.0"
        boolean is_active
        timestamp last_checked
        integer total_reports
        integer verified_reports
    }

    verifications {
        bigint id PK
        bigint conflict_event_id FK
        bigint source_id FK
        varchar source_url
        varchar source_title
        text source_excerpt
        timestamp verified_at
        varchar verification_method "auto|manual"
    }

    users {
        bigint id PK
        varchar email UK
        varchar password_hash
        varchar username
        boolean email_verified
        varchar role "free|premium|admin"
        timestamp created_at
        timestamp last_login
        boolean is_active
    }

    alerts {
        bigint id PK
        bigint user_id FK
        varchar region_filter "JSON"
        varchar conflict_type_filter "JSON array"
        integer severity_threshold "1-5"
        varchar notification_method "push|email|rss"
        boolean is_active
        timestamp created_at
        timestamp last_triggered
    }

    regions {
        bigint id PK
        varchar name
        varchar country_code
        geometry boundary "PostGIS POLYGON"
        varchar region_type "country|province|custom"
    }

    bookmarks {
        bigint id PK
        bigint user_id FK
        bigint conflict_event_id FK
        timestamp created_at
    }

    user_preferences {
        bigint id PK
        bigint user_id FK
        varchar theme "light|dark"
        varchar default_map_view "JSON"
        varchar export_format "csv|json"
        boolean email_notifications
        boolean push_notifications
        varchar quiet_hours_start "time"
        varchar quiet_hours_end "time"
    }
```

### Tables

#### conflict_events

Core table storing all conflict events.

```sql
CREATE TABLE conflict_events (
    id BIGSERIAL PRIMARY KEY,
    location GEOGRAPHY(POINT, 4326) NOT NULL,
    location_display GEOGRAPHY(POINT, 4326), -- Blurred coordinates for safety
    event_type VARCHAR(50) NOT NULL,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    severity_score INTEGER CHECK (severity_score BETWEEN 1 AND 5),
    casualties_min INTEGER DEFAULT 0,
    casualties_max INTEGER,
    event_timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    verification_status VARCHAR(20) DEFAULT 'unverified',
    confidence_score FLOAT CHECK (confidence_score BETWEEN 0.0 AND 1.0),
    is_active BOOLEAN DEFAULT TRUE,
    actors_involved JSONB DEFAULT '[]',
    country_code VARCHAR(2),
    region_name VARCHAR(200),
    ai_summary TEXT,
    conflict_id VARCHAR(100), -- Group related events
    CONSTRAINT valid_severity CHECK (severity_score BETWEEN 1 AND 5),
    CONSTRAINT valid_confidence CHECK (confidence_score BETWEEN 0.0 AND 1.0)
);
```

**Indexes:**
```sql
-- Geospatial index for location-based queries
CREATE INDEX idx_conflict_events_location ON conflict_events USING GIST (location);

-- Composite index for filtering
CREATE INDEX idx_conflict_events_active_severity ON conflict_events (is_active, severity_score DESC);

-- Temporal index for time-range queries
CREATE INDEX idx_conflict_events_timestamp ON conflict_events (event_timestamp DESC);

-- Text search index
CREATE INDEX idx_conflict_events_title_search ON conflict_events USING GIN (to_tsvector('english', title));
CREATE INDEX idx_conflict_events_description_search ON conflict_events USING GIN (to_tsvector('english', description));

-- Region/country filtering
CREATE INDEX idx_conflict_events_country ON conflict_events (country_code);
CREATE INDEX idx_conflict_events_region ON conflict_events (region_name);

-- Event type filtering
CREATE INDEX idx_conflict_events_type ON conflict_events (event_type);

-- Composite index for common query pattern
CREATE INDEX idx_conflict_events_map_view ON conflict_events (is_active, event_timestamp DESC, severity_score DESC) WHERE is_active = TRUE;
```

#### sources

Metadata about data sources and their credibility.

```sql
CREATE TABLE sources (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL UNIQUE,
    url VARCHAR(500),
    source_type VARCHAR(20) NOT NULL, -- api, rss, manual, social
    credibility_tier INTEGER CHECK (credibility_tier BETWEEN 1 AND 4),
    credibility_score FLOAT DEFAULT 0.5 CHECK (credibility_score BETWEEN 0.0 AND 1.0),
    is_active BOOLEAN DEFAULT TRUE,
    last_checked TIMESTAMP WITH TIME ZONE,
    total_reports INTEGER DEFAULT 0,
    verified_reports INTEGER DEFAULT 0,
    api_endpoint VARCHAR(500),
    api_key_encrypted BYTEA, -- Encrypted API key if needed
    polling_interval_seconds INTEGER DEFAULT 300,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT valid_tier CHECK (credibility_tier BETWEEN 1 AND 4)
);
```

**Indexes:**
```sql
CREATE INDEX idx_sources_active ON sources (is_active);
CREATE INDEX idx_sources_tier ON sources (credibility_tier);
```

#### verifications

Track which sources reported each conflict event.

```sql
CREATE TABLE verifications (
    id BIGSERIAL PRIMARY KEY,
    conflict_event_id BIGINT NOT NULL REFERENCES conflict_events(id) ON DELETE CASCADE,
    source_id BIGINT NOT NULL REFERENCES sources(id),
    source_url VARCHAR(1000),
    source_title VARCHAR(500),
    source_excerpt TEXT,
    verified_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    verification_method VARCHAR(20) DEFAULT 'auto', -- auto, manual
    source_casualties_min INTEGER,
    source_casualties_max INTEGER,
    UNIQUE(conflict_event_id, source_id)
);
```

**Indexes:**
```sql
CREATE INDEX idx_verifications_event ON verifications (conflict_event_id);
CREATE INDEX idx_verifications_source ON verifications (source_id);
CREATE INDEX idx_verifications_method ON verifications (verification_method);
```

#### users

User accounts for personalized features.

```sql
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255), -- NULL for OAuth-only users
    username VARCHAR(100) UNIQUE,
    email_verified BOOLEAN DEFAULT FALSE,
    role VARCHAR(20) DEFAULT 'free', -- free, premium, admin
    oauth_provider VARCHAR(50), -- google, github, null for email auth
    oauth_id VARCHAR(255), -- Provider's user ID
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_login TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT TRUE,
    failed_login_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP WITH TIME ZONE
);
```

**Indexes:**
```sql
CREATE INDEX idx_users_email ON users (email);
CREATE INDEX idx_users_role ON users (role);
CREATE INDEX idx_users_active ON users (is_active);
```

#### alerts

User-configured alert preferences.

```sql
CREATE TABLE alerts (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(200),
    region_filter JSONB, -- {country_codes: [...], region_names: [...]}
    conflict_type_filter JSONB, -- Array of event types
    severity_threshold INTEGER DEFAULT 3 CHECK (severity_threshold BETWEEN 1 AND 5),
    notification_method VARCHAR(20) DEFAULT 'push', -- push, email, rss
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_triggered TIMESTAMP WITH TIME ZONE,
    trigger_count INTEGER DEFAULT 0,
    CONSTRAINT valid_severity_threshold CHECK (severity_threshold BETWEEN 1 AND 5)
);
```

**Indexes:**
```sql
CREATE INDEX idx_alerts_user ON alerts (user_id);
CREATE INDEX idx_alerts_active ON alerts (is_active);
CREATE INDEX idx_alerts_severity ON alerts (severity_threshold);
```

#### regions

Geographic regions for filtering and organization.

```sql
CREATE TABLE regions (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    country_code VARCHAR(2),
    boundary GEOGRAPHY(POLYGON, 4326),
    region_type VARCHAR(50) DEFAULT 'country', -- country, province, custom
    parent_region_id BIGINT REFERENCES regions(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

**Indexes:**
```sql
CREATE INDEX idx_regions_boundary ON regions USING GIST (boundary);
CREATE INDEX idx_regions_country ON regions (country_code);
CREATE INDEX idx_regions_type ON regions (region_type);
```

#### bookmarks

User-saved conflict events.

```sql
CREATE TABLE bookmarks (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    conflict_event_id BIGINT NOT NULL REFERENCES conflict_events(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, conflict_event_id)
);
```

**Indexes:**
```sql
CREATE INDEX idx_bookmarks_user ON bookmarks (user_id);
CREATE INDEX idx_bookmarks_event ON bookmarks (conflict_event_id);
```

#### user_preferences

User settings and preferences.

```sql
CREATE TABLE user_preferences (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    theme VARCHAR(20) DEFAULT 'light', -- light, dark
    default_map_view JSONB, -- {lat, lng, zoom}
    export_format VARCHAR(10) DEFAULT 'json', -- csv, json
    email_notifications BOOLEAN DEFAULT TRUE,
    push_notifications BOOLEAN DEFAULT TRUE,
    quiet_hours_start TIME,
    quiet_hours_end TIME,
    language VARCHAR(10) DEFAULT 'en',
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Indexes Summary

| Index Name | Table | Columns | Type | Rationale |
|------------|-------|---------|------|-----------|
| `idx_conflict_events_location` | conflict_events | location | GIST | Fast geospatial queries for map rendering |
| `idx_conflict_events_active_severity` | conflict_events | is_active, severity_score | B-tree | Filter active events by severity |
| `idx_conflict_events_timestamp` | conflict_events | event_timestamp | B-tree | Time-range queries for timeline views |
| `idx_conflict_events_title_search` | conflict_events | title | GIN | Full-text search |
| `idx_conflict_events_map_view` | conflict_events | Multiple | B-tree (partial) | Optimize common map view query |
| `idx_sources_active` | sources | is_active | B-tree | Filter active sources |
| `idx_verifications_event` | verifications | conflict_event_id | B-tree | Lookup all sources for an event |
| `idx_alerts_user` | alerts | user_id | B-tree | Fetch user's alerts |
| `idx_regions_boundary` | regions | boundary | GIST | Spatial queries for region containment |

## Backend Architecture

### Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration and settings
│   ├── database.py             # Database connection and session management
│   │
│   ├── api/                    # API routers
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── events.py       # Conflict event endpoints
│   │   │   ├── sources.py      # Source management endpoints
│   │   │   ├── alerts.py       # User alert endpoints
│   │   │   ├── users.py        # User authentication endpoints
│   │   │   ├── regions.py      # Geographic region endpoints
│   │   │   └── export.py       # Data export endpoints
│   │   └── deps.py             # Dependency injection (auth, rate limiting)
│   │
│   ├── models/                 # SQLAlchemy database models
│   │   ├── __init__.py
│   │   ├── conflict_event.py
│   │   ├── source.py
│   │   ├── verification.py
│   │   ├── user.py
│   │   ├── alert.py
│   │   └── region.py
│   │
│   ├── schemas/                # Pydantic schemas for validation
│   │   ├── __init__.py
│   │   ├── event.py
│   │   ├── source.py
│   │   ├── user.py
│   │   └── alert.py
│   │
│   ├── services/               # Business logic
│   │   ├── __init__.py
│   │   ├── event_service.py    # Event CRUD and queries
│   │   ├── verification_service.py  # Multi-source verification
│   │   ├── alert_service.py    # Alert triggering and notifications
│   │   ├── geospatial_service.py  # Location processing and blurring
│   │   └── ai_service.py       # Ollama integration
│   │
│   ├── collectors/             # Data source collectors
│   │   ├── __init__.py
│   │   ├── base_collector.py   # Abstract base class
│   │   ├── gdelt_collector.py
│   │   ├── acled_collector.py
│   │   ├── newsapi_collector.py
│   │   ├── unocha_collector.py
│   │   └── social_collector.py
│   │
│   ├── pipelines/              # Data processing pipelines
│   │   ├── __init__.py
│   │   ├── normalizer.py       # Data normalization
│   │   ├── deduplication.py    # Duplicate detection
│   │   └── verification.py     # Multi-source verification
│   │
│   ├── utils/                  # Utility functions
│   │   ├── __init__.py
│   │   ├── security.py         # Password hashing, JWT
│   │   ├── rate_limiter.py     # Rate limiting logic
│   │   └── logging.py          # Structured logging setup
│   │
│   └── workers/                # Celery workers
│       ├── __init__.py
│       ├── celery_app.py       # Celery configuration
│       └── tasks.py            # Async tasks
│
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── conftest.py             # Pytest fixtures
│   ├── test_api/
│   ├── test_services/
│   ├── test_collectors/
│   └── test_pipelines/
│
├── alembic/                    # Database migrations
│   ├── versions/
│   └── env.py
│
├── requirements.txt            # Python dependencies
├── requirements-dev.txt        # Development dependencies
├── Dockerfile                  # Backend container
└── pytest.ini                  # Pytest configuration
```

### API Design

RESTful API with versioning (`/api/v1/`). All responses are JSON.

#### Authentication Endpoints

```
POST   /api/v1/auth/register          # Register new user
POST   /api/v1/auth/login             # Login (email/password)
POST   /api/v1/auth/oauth/{provider}  # OAuth login (google, github)
POST   /api/v1/auth/refresh           # Refresh JWT token
POST   /api/v1/auth/logout            # Logout (invalidate token)
GET    /api/v1/auth/me                # Get current user profile
```

#### Conflict Event Endpoints

```
GET    /api/v1/events                 # List events (with filters)
GET    /api/v1/events/{id}            # Get event details
GET    /api/v1/events/nearby          # Events near coordinates
GET    /api/v1/events/timeline        # Events in time range
GET    /api/v1/events/stats           # Aggregate statistics
POST   /api/v1/events                 # Manual event entry (admin only)
PUT    /api/v1/events/{id}            # Update event (admin only)
DELETE /api/v1/events/{id}            # Delete event (admin only)
```

**Query Parameters for GET /api/v1/events:**
- `lat`, `lng`, `radius` - Geospatial filter
- `severity_min`, `severity_max` - Severity range
- `event_type` - Filter by type (armed_conflict, protest, terrorism, etc.)
- `date_from`, `date_to` - Date range
- `country` - Country code filter
- `verified` - Filter by verification status
- `limit`, `offset` - Pagination

#### Alert Endpoints (Authenticated)

```
GET    /api/v1/alerts                 # List user's alerts
POST   /api/v1/alerts                 # Create new alert
PUT    /api/v1/alerts/{id}            # Update alert
DELETE /api/v1/alerts/{id}            # Delete alert
POST   /api/v1/alerts/{id}/test       # Test alert notification
```

#### User Endpoints (Authenticated)

```
GET    /api/v1/users/me               # Get profile
PUT    /api/v1/users/me               # Update profile
GET    /api/v1/users/me/preferences   # Get preferences
PUT    /api/v1/users/me/preferences   # Update preferences
GET    /api/v1/users/me/bookmarks     # Get bookmarks
POST   /api/v1/users/me/bookmarks     # Add bookmark
DELETE /api/v1/users/me/bookmarks/{event_id}  # Remove bookmark
```

#### Export Endpoints

```
GET    /api/v1/export/csv             # Export filtered events as CSV
GET    /api/v1/export/json            # Export filtered events as JSON
GET    /api/v1/export/rss/{alert_id}  # RSS feed for alert
```

#### Source Management (Admin)

```
GET    /api/v1/sources                # List all sources
GET    /api/v1/sources/{id}           # Get source details
PUT    /api/v1/sources/{id}           # Update source
GET    /api/v1/sources/stats          # Source performance statistics
```

#### Regions

```
GET    /api/v1/regions                # List regions
GET    /api/v1/regions/{id}           # Get region details
GET    /api/v1/regions/{id}/events    # Events in region
```

### API Response Format

**Success Response:**
```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "total": 100,
    "page": 1,
    "per_page": 20
  }
}
```

**Error Response:**
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {"field": "email", "message": "Invalid email format"}
    ]
  }
}
```

### Data Collectors

Each data source has a dedicated collector implementing the `BaseCollector` abstract class.

**Collector Architecture:**
```python
# Abstract base class
class BaseCollector(ABC):
    @abstractmethod
    async def fetch(self) -> List[RawEvent]:
        """Fetch raw data from source"""
        pass
    
    @abstractmethod
    def parse(self, raw_data: Any) -> List[RawEvent]:
        """Parse raw data into standardized format"""
        pass
    
    async def run(self):
        """Main collector loop with error handling"""
        try:
            raw = await self.fetch()
            events = self.parse(raw)
            await self.send_to_queue(events)
        except Exception as e:
            await self.handle_error(e)
```

**Collector Features:**
- **Rate limiting**: Respect API rate limits per source
- **Retry logic**: Exponential backoff on failures (3 retries)
- **Error handling**: Log errors, continue processing other sources
- **Health monitoring**: Track last successful fetch, failure count
- **Circuit breaker**: Disable source after consecutive failures

**Collector Schedule:**
| Source | Polling Interval | Priority |
|--------|-----------------|----------|
| GDELT | 5 minutes | High |
| ACLED | 5 minutes | High |
| NewsAPI | 10 minutes | Medium |
| UN OCHA | 30 minutes | Medium |
| Government RSS | 60 minutes | Low |
| Social Media | 2 minutes | High (for breaking events) |

### Verification Pipeline

Multi-stage async pipeline for cross-source verification.

**Pipeline Stages:**

1. **Normalization**: Convert all events to unified schema
2. **Deduplication**: Identify duplicate events using fuzzy matching
3. **Correlation**: Match events across sources
4. **Scoring**: Calculate confidence score based on:
   - Number of independent sources
   - Source credibility tiers
   - Agreement on key details (location, casualties, event type)
5. **Classification**: AI-powered event type classification
6. **Summarization**: AI-generated 2-3 sentence summary

**Verification Algorithm:**
```python
async def verify_event(event: NormalizedEvent) -> VerifiedEvent:
    # Find similar events within time window (±2 hours)
    similar_events = await find_similar_events(
        location=event.location,
        timestamp=event.timestamp,
        event_type=event.event_type,
        radius_km=50,
        time_window_hours=2
    )
    
    # Group by likely same event
    clusters = cluster_events(similar_events)
    
    # Calculate confidence score
    confidence = calculate_confidence(
        source_count=len(clusters.sources),
        source_tiers=clusters.source_tiers,
        agreement_score=clusters.agreement_on_details
    )
    
    # Determine verification status
    if confidence >= 0.8 and len(clusters.sources) >= 3:
        status = "verified"
    elif confidence >= 0.5:
        status = "developing"
    else:
        status = "unverified"
    
    return VerifiedEvent(
        **event.dict(),
        confidence_score=confidence,
        verification_status=status,
        source_count=len(clusters.sources)
    )
```

**Confidence Score Calculation:**
```
confidence = (
    0.4 * source_diversity_score +      # More sources = higher confidence
    0.3 * source_credibility_score +     # Tier 1 sources weighted higher
    0.3 * detail_agreement_score         # Agreement on casualties, location, etc.
)
```

### Caching Strategy

Multi-layer caching with Redis.

**Cache Layers:**

1. **L1 - Application Cache** (In-memory, per-instance)
   - Frequently accessed configuration
   - User session data (short-lived)
   - TTL: 1-5 minutes

2. **L2 - Redis Cache** (Shared across instances)
   - API responses (events list, statistics)
   - Geospatial query results
   - User preferences
   - TTL: 5-30 minutes depending on data freshness requirements

3. **L3 - Database Materialized Views** (PostgreSQL)
   - Aggregate statistics (event counts by region, type)
   - Trend data (7-day, 30-day comparisons)
   - Refresh: Every 15 minutes via scheduled job

**Cache Keys Pattern:**
```
events:list:{filters_hash}          # Event list with filters
events:{id}                          # Single event details
stats:global                         # Global statistics
stats:region:{region_id}             # Region-specific stats
user:{id}:preferences                # User preferences
source:{id}:last_check               # Source last check timestamp
```

**Cache Invalidation:**
- **Write-through**: Update cache on data writes
- **TTL-based**: Automatic expiration
- **Manual invalidation**: Admin actions, data corrections
- **Tag-based invalidation**: Invalidate all caches tagged with `region:{id}`

**Redis Data Structures:**
- **Strings**: Simple key-value (user preferences, sessions)
- **Hashes**: Object storage (event details)
- **Sets**: Unique collections (active event IDs)
- **Sorted Sets**: Leaderboards (trending conflicts)
- **Geo**: Geospatial queries (nearby events)

## Frontend Architecture

### Project Structure

```
frontend/
├── app/                        # Next.js App Router
│   ├── layout.tsx              # Root layout
│   ├── page.tsx                # Home page (map dashboard)
│   ├── globals.css             # Global styles
│   │
│   ├── (public)/               # Public routes (no auth required)
│   │   ├── map/
│   │   │   └── page.tsx        # Interactive map view
│   │   ├── timeline/
│   │   │   └── page.tsx        # Timeline view
│   │   └── about/
│   │       └── page.tsx        # About page
│   │
│   ├── (auth)/                 # Authentication routes
│   │   ├── login/
│   │   │   └── page.tsx        # Login page
│   │   ├── register/
│   │   │   └── page.tsx        # Registration page
│   │   └── oauth/
│   │       └── callback/
│   │           └── route.tsx   # OAuth callback handler
│   │
│   └── (dashboard)/            # Authenticated routes
│       ├── layout.tsx          # Dashboard layout with sidebar
│       ├── dashboard/
│       │   └── page.tsx        # User dashboard
│       ├── alerts/
│       │   ├── page.tsx        # Alert management
│       │   └── create/
│       │       └── page.tsx    # Create alert form
│       ├── bookmarks/
│       │   └── page.tsx        # Saved conflicts
│       ├── settings/
│       │   └── page.tsx        # User settings
│       └── api/                # API routes (Next.js server-side)
│           └── proxy/          # Backend API proxy
│
├── components/                 # React components
│   ├── ui/                     # Base UI components
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── dialog.tsx
│   │   ├── input.tsx
│   │   ├── select.tsx
│   │   └── ...
│   │
│   ├── map/                    # Map-related components
│   │   ├── conflict-map.tsx    # Main interactive map
│   │   ├── event-marker.tsx    # Map marker for events
│   │   ├── marker-cluster.tsx  # Clustered markers
│   │   ├── map-controls.tsx    # Zoom, filter controls
│   │   └── map-legend.tsx      # Severity legend
│   │
│   ├── events/                 # Event display components
│   │   ├── event-card.tsx      # Event summary card
│   │   ├── event-detail.tsx    # Full event details panel
│   │   ├── event-list.tsx      # List of events
│   │   ├── event-timeline.tsx  # Timeline visualization
│   │   └── source-list.tsx     # Source verification badges
│   │
│   ├── filters/                # Filter components
│   │   ├── filter-panel.tsx    # Main filter sidebar
│   │   ├── severity-filter.tsx
│   │   ├── type-filter.tsx
│   │   ├── date-filter.tsx
│   │   └── region-filter.tsx
│   │
│   ├── alerts/                 # Alert components
│   │   ├── alert-form.tsx
│   │   ├── alert-list.tsx
│   │   └── alert-card.tsx
│   │
│   └── layout/                 # Layout components
│       ├── header.tsx
│       ├── footer.tsx
│       ├── sidebar.tsx
│       └── navigation.tsx
│
├── context/                    # React Context providers
│   ├── auth-context.tsx        # Authentication state
│   ├── map-context.tsx         # Map state (view, filters)
│   └── theme-context.tsx       # Dark/light mode
│
├── lib/                        # Utility libraries
│   ├── api.ts                  # API client (axios/fetch)
│   ├── websocket.ts            # WebSocket connection
│   ├── utils.ts                # Helper functions
│   ├── constants.ts            # App constants
│   └── validations.ts          # Zod schemas
│
├── hooks/                      # Custom React hooks
│   ├── use-events.ts           # Fetch and manage events
│   ├── use-alerts.ts           # Alert management
│   ├── use-auth.ts             # Authentication hooks
│   ├── use-map.ts              # Map interactions
│   └── use-websocket.ts        # Real-time updates
│
├── stores/                     # Zustand stores
│   ├── event-store.ts          # Event state management
│   ├── filter-store.ts         # Filter state
│   └── user-store.ts           # User state
│
├── types/                      # TypeScript types
│   ├── event.ts
│   ├── user.ts
│   ├── alert.ts
│   └── api.ts
│
├── public/                     # Static assets
│   ├── images/
│   ├── icons/
│   └── locales/                # i18n files (future)
│
├── styles/                     # Additional styles
│   └── map.css                 # Map-specific styles
│
├── tests/                      # Test files
│   ├── components/
│   ├── hooks/
│   └── utils/
│
├── next.config.js              # Next.js configuration
├── tailwind.config.js          # Tailwind configuration
├── tsconfig.json               # TypeScript configuration
├── package.json
└── Dockerfile
```

### Component Hierarchy

```mermaid
graph TD
    App[App Root] --> Layout[Root Layout]
    Layout --> Header[Header]
    Layout --> Main[Main Content]
    Layout --> Footer[Footer]
    
    Main --> MapPage[Map Dashboard]
    MapPage --> FilterPanel[Filter Panel]
    MapPage --> ConflictMap[Conflict Map]
    MapPage --> EventList[Event List Sidebar]
    
    ConflictMap --> MapLibre[MapLibre GL]
    ConflictMap --> EventMarkers[Event Markers]
    ConflictMap --> MapControls[Map Controls]
    ConflictMap --> MapLegend[Map Legend]
    
    EventMarkers --> MarkerCluster[Marker Clustering]
    EventMarkers --> EventMarker[Individual Marker]
    
    EventList --> EventCard[Event Card]
    EventCard --> EventDetail[Event Detail Panel]
    EventDetail --> SourceList[Source List]
    EventDetail --> Timeline[Event Timeline]
    
    FilterPanel --> SeverityFilter[Severity Filter]
    FilterPanel --> TypeFilter[Event Type Filter]
    FilterPanel --> DateFilter[Date Range Filter]
    FilterPanel --> RegionFilter[Region Filter]
    
    Header --> Auth[Auth Buttons]
    Header --> ThemeToggle[Theme Toggle]
    Header --> Navigation[Navigation]
    
    style ConflictMap fill:#e3f2fd
    style EventDetail fill:#fff3e0
    style FilterPanel fill:#f3e5f5
```

### State Management

**Zustand for Client State:**
- Event filters (severity, type, date range, region)
- Map view state (center, zoom, bounds)
- UI state (sidebar open/close, selected event)
- User preferences (theme, notification settings)

**React Query for Server State:**
- Event data (with caching and background refresh)
- User data (profile, alerts, bookmarks)
- Source metadata
- Statistics and aggregates

**Why Zustand over Redux:**
- Simpler API, less boilerplate
- Sufficient for our state complexity
- Better TypeScript support
- Smaller bundle size

**Why React Query:**
- Built-in caching and deduplication
- Background refetch on focus/reconnect
- Optimistic updates
- Pagination support
- Reduces need for manual state management

### Map Integration

**Library Choice: MapLibre GL**

**Rationale:**
- Open-source (no licensing costs vs. Mapbox)
- Vector tiles (better performance than raster)
- Active community and maintenance
- Supports PostGIS-compatible coordinate systems
- Customizable styling

**Implementation Approach:**

```typescript
// Core map component
const ConflictMap: React.FC = () => {
  const mapRef = useRef<maplibregl.Map | null>(null);
  const { events, filters } = useEventStore();
  
  // Initialize map
  useEffect(() => {
    mapRef.current = new maplibregl.Map({
      container: 'map-container',
      style: 'https://demotiles.maplibre.org/style.json',
      center: [0, 20],
      zoom: 2,
    });
    
    // Add controls
    mapRef.current.addControl(new maplibregl.NavigationControl());
    mapRef.current.addControl(new maplibregl.ScaleControl());
    
    return () => mapRef.current?.remove();
  }, []);
  
  // Render event markers
  useEffect(() => {
    if (!mapRef.current || !events.length) return;
    
    // Clear existing markers
    clearMarkers();
    
    // Add new markers with clustering
    const markers = createEventMarkers(events, filters);
    addMarkersToMap(markers);
    
  }, [events, filters]);
  
  return <div id="map-container" className="w-full h-full" />;
};
```

**Marker Clustering:**
- Use `supercluster` library for client-side clustering
- Cluster at low zoom levels, show individual markers when zoomed in
- Cluster size indicates number of events
- Color indicates highest severity in cluster

**Performance Optimizations:**
- Only render events in current viewport
- Debounce map move/zoom events
- Use Web Workers for clustering calculations
- Limit max markers rendered (show "zoom in for more" when exceeded)

**Custom Map Styling:**
- Neutral base map (no political boundaries emphasized)
- Custom severity color scheme (green → yellow → orange → red → dark red)
- Accessibility: Add icons/patterns for colorblind users
- Dark mode support

### Real-time Updates

**WebSocket Implementation:**

```typescript
// WebSocket hook
const useWebSocket = () => {
  const [connected, setConnected] = useState(false);
  const eventStore = useEventStore();
  
  useEffect(() => {
    const ws = new WebSocket(`${WS_URL}/ws/events`);
    
    ws.onopen = () => setConnected(true);
    ws.onclose = () => setConnected(false);
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      switch (data.type) {
        case 'NEW_EVENT':
          eventStore.addEvent(data.payload);
          showNotification('New conflict event detected');
          break;
        case 'EVENT_UPDATED':
          eventStore.updateEvent(data.payload);
          break;
        case 'EVENT_VERIFIED':
          eventStore.updateEvent(data.payload);
          showNotification('Event verified by multiple sources');
          break;
        case 'SEVERITY_ESCALATION':
          eventStore.updateEvent(data.payload);
          showNotification('Conflict severity escalated', 'warning');
          break;
      }
    };
    
    return () => ws.close();
  }, []);
  
  return { connected };
};
```

**Fallback: Polling**
- If WebSocket unavailable, fall back to polling every 30 seconds
- Use `If-Modified-Since` header to reduce bandwidth
- Only fetch changed events (delta sync)

## Data Flow

### Collection → Processing → Storage

```mermaid
sequenceDiagram
    participant Source as Data Source
    participant Collector as Collector
    participant Queue as Redis Queue
    participant Normalizer as Normalizer
    participant Dedup as Deduplication
    participant Verifier as Verification
    participant AI as AI Service
    participant DB as PostgreSQL
    participant Cache as Redis Cache
    
    Source->>Collector: New data available
    Collector->>Collector: Fetch data (with rate limiting)
    Collector->>Queue: Push raw events
    Queue->>Normalizer: Consume raw events
    Normalizer->>Normalizer: Parse and normalize schema
    Normalizer->>Dedup: Send normalized events
    Dedup->>Dedup: Fuzzy matching
    Dedup->>Verifier: Send unique events
    Verifier->>Verifier: Cross-source correlation
    Verifier->>AI: Request classification & summary
    AI->>Verifier: Return AI results
    Verifier->>DB: Store verified event
    Verifier->>Cache: Invalidate related caches
    Verifier->>Cache: Update statistics
```

**Step-by-step:**

1. **Collection** (Async, parallel)
   - Each collector runs on independent schedule
   - Fetches data from source API/RSS
   - Handles rate limiting and errors
   - Pushes raw data to Redis queue

2. **Normalization** (Async worker)
   - Consumes from Redis queue
   - Parses source-specific format
   - Maps to unified schema
   - Validates required fields
   - Extracts geolocation (NLP for location names)

3. **Deduplication** (Async worker)
   - Compares against recent events (±2 hours)
   - Geospatial proximity check (50km radius)
   - Fuzzy matching on title/description
   - Merges duplicate reports

4. **Verification** (Async worker)
   - Correlates events across sources
   - Calculates confidence score
   - Determines verification status
   - Links source metadata

5. **AI Processing** (Ollama Cloud)
   - Classifies event type
   - Generates 2-3 sentence summary
   - Detects potential misinformation
   - Extracts actors involved

6. **Storage**
   - Inserts into PostgreSQL with PostGIS
   - Triggers cache invalidation
   - Updates materialized views
   - Sends WebSocket notification to connected clients

### User Request → Response

```mermaid
sequenceDiagram
    participant User
    participant Frontend as Next.js
    participant API as FastAPI
    participant Auth as Auth Service
    participant Cache as Redis
    participant DB as PostgreSQL
    
    User->>Frontend: Load map dashboard
    Frontend->>API: GET /api/v1/events?filters
    API->>Auth: Validate JWT token
    Auth-->>API: Token valid
    API->>Cache: Check cache for query
    alt Cache hit
        Cache-->>API: Cached response
    else Cache miss
        API->>DB: Query events with filters
        DB-->>API: Event data
        API->>Cache: Store in cache (TTL: 5 min)
    end
    API-->>Frontend: JSON response
    Frontend->>Frontend: Render map markers
    Frontend-->>User: Display interactive map
    
    Note over API,Frontend: Real-time updates via WebSocket
    API->>Frontend: WebSocket: NEW_EVENT
    Frontend->>Frontend: Update map markers
    Frontend-->>User: Show notification
```

## Security Architecture

### Authentication

**JWT-based Authentication:**
- Access tokens: 15-minute expiry
- Refresh tokens: 7-day expiry (stored in HTTP-only cookie)
- Token signing: RS256 (asymmetric)
- Token storage: Memory (access), HTTP-only cookie (refresh)

**OAuth Integration:**
- Google OAuth 2.0
- GitHub OAuth
- Account linking (OAuth + email)

**Password Security:**
- bcrypt hashing (cost factor: 12)
- Password requirements: 12+ characters, complexity
- Account lockout: 5 failed attempts → 15-minute lock
- Password reset: Time-limited tokens (1 hour)

**Implementation:**
```python
# JWT token creation
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    encoded_jwt = jwt.encode(to_encode, PRIVATE_KEY, algorithm="RS256")
    return encoded_jwt

# Dependency for protected routes
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401)
    except jwt.PyJWTError:
        raise HTTPException(status_code=401)
    
    user = await get_user_by_id(user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=401)
    return user
```

### Rate Limiting

**Strategy:** Token bucket algorithm with Redis

**Limits:**
| Endpoint Type | Free Tier | Premium Tier |
|--------------|-----------|--------------|
| Event queries | 100/hour | 1000/hour |
| Alert creation | 10/day | 100/day |
| Export requests | 5/day | 50/day |
| Authentication | 10/minute (per IP) | 10/minute (per IP) |

**Implementation:**
```python
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

# Initialize on startup
@app.on_event("startup")
async def startup():
    redis = await aioredis.from_url(REDIS_URL)
    await FastAPILimiter.init(redis)

# Apply to endpoints
@app.get("/api/v1/events", dependencies=[Depends(RateLimiter(times=100, seconds=3600))])
async def get_events():
    ...
```

**DDoS Protection:**
- Cloudflare or AWS Shield in front of application
- IP-based rate limiting at edge
- Geographic blocking if needed (for abuse mitigation)

### Input Validation

**Pydantic Models:**
```python
class EventFilterSchema(BaseModel):
    lat: Optional[float] = Field(None, ge=-90, le=90)
    lng: Optional[float] = Field(None, ge=-180, le=180)
    radius: Optional[float] = Field(None, ge=0, le=10000)  # km
    severity_min: Optional[int] = Field(None, ge=1, le=5)
    severity_max: Optional[int] = Field(None, ge=1, le=5)
    event_type: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    country: Optional[str] = Field(None, min_length=2, max_length=2)
    limit: Optional[int] = Field(50, ge=1, le=500)
    offset: Optional[int] = Field(0, ge=0)
    
    @validator('date_to')
    def date_to_not_before_from(cls, v, values):
        if v and values.get('date_from') and v < values['date_from']:
            raise ValueError('date_to must be after date_from')
        return v
```

**SQL Injection Prevention:**
- SQLAlchemy ORM (parameterized queries)
- No raw SQL queries
- Input sanitization for search terms

**XSS Prevention:**
- React escapes output by default
- Content Security Policy headers
- No `dangerouslySetInnerHTML` except with sanitization (DOMPurify)

### CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://wartracker.org",  # Production
        "https://www.wartracker.org",
        "http://localhost:3000",   # Development
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
    expose_headers=["X-RateLimit-Remaining", "X-RateLimit-Reset"],
)
```

### Data Sanitization

- **User-generated content** (manual event entries): HTML sanitization, link stripping
- **Source data**: Strip scripts, validate URLs
- **Export data**: CSV injection prevention (prefix with tab)

## Performance & Scalability

### Caching Layers

**Three-tier caching strategy:**

```
┌─────────────────────────────────────┐
│  L1: Application Cache (In-memory)  │  TTL: 1-5 min
│  - User sessions                    │
│  - Config values                    │
│  - Frequently accessed objects      │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  L2: Redis Cache (Shared)           │  TTL: 5-30 min
│  - API responses                    │
│  - Geospatial query results         │
│  - User preferences                 │
│  - Aggregated statistics            │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  L3: Materialized Views (PostgreSQL)│  Refresh: 15 min
│  - Global statistics                │
│  - Regional aggregates              │
│  - Trend data                       │
└─────────────────────────────────────┘
```

**Cache Hit Targets:**
- Event list queries: ≥80% hit rate
- Single event lookups: ≥90% hit rate
- Statistics: ≥95% hit rate

### Database Optimization

**Indexing Strategy:**
- Geospatial: GIST indexes on all location columns
- Temporal: B-tree on timestamps for range queries
- Text: GIN indexes for full-text search
- Composite: Covering indexes for common query patterns

**Query Optimization:**
- Use `EXPLAIN ANALYZE` for slow queries
- Avoid `SELECT *`, fetch only needed columns
- Use covering indexes where possible
- Batch queries when possible

**Partitioning:**
- Partition `conflict_events` table by year
- Improves query performance for historical data
- Simplifies data retention (drop old partitions)

```sql
CREATE TABLE conflict_events (
    ...
) PARTITION BY RANGE (event_timestamp);

CREATE TABLE conflict_events_2024 PARTITION OF conflict_events
    FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
```

**Connection Pooling:**
- PgBouncer for connection pooling
- Pool size: 20 connections per backend instance
- Prevents connection exhaustion under load

### Horizontal Scaling

**Stateless Backend:**
- No session affinity required
- Any instance can handle any request
- Scale based on CPU/memory metrics

**Database Scaling:**
- Read replicas for read-heavy workloads
- Primary for writes only
- Connection pooling per replica

**Caching Layer:**
- Redis Cluster for horizontal scaling
- Shard by key prefix
- Automatic failover

**CDN:**
- Cloudflare or AWS CloudFront
- Cache static assets (JS, CSS, images)
- Cache API responses (public endpoints)
- Edge computing for geolocation

**Scaling Triggers:**
- CPU > 70% for 5 minutes → Scale up
- Memory > 80% for 5 minutes → Scale up
- Request queue depth > 100 → Scale up
- Response time p95 > 500ms → Investigate

## Ethical Safeguards

### Coordinate Blurring

**Implementation:**
```python
def blur_coordinates(lat: float, lng: float, severity: int, is_active: bool) -> Tuple[float, float]:
    """
    Blur coordinates for safety based on severity and activity status.
    
    Blurring levels:
    - Severity 1-2 (low): No blurring (100m precision)
    - Severity 3 (medium): City-level (5km precision)
    - Severity 4-5 (high): Regional (50km precision)
    - Active conflicts: Additional 24-hour delay
    """
    if not is_active or severity <= 2:
        # High precision for historical/low-severity
        return lat, lng
    
    # Add random offset
    max_offset = 0.05 if severity == 3 else 0.5  # ~5km or ~50km
    
    blurred_lat = lat + random.uniform(-max_offset, max_offset)
    blurred_lng = lng + random.uniform(-max_offset, max_offset)
    
    return blurred_lat, blurred_lng
```

**Policy:**
- Display blurred coordinates in public API
- Store precise coordinates in database (for research access)
- Researchers can request precise data with approval
- Time delay (24-48 hours) for active high-severity conflicts

### Bias Mitigation

**Source Diversity:**
- Minimum 3 sources from different regions
- Actively include Global South sources
- Track source geographic distribution
- Quarterly bias audit

**Algorithm Transparency:**
- Publish verification methodology
- Document source credibility criteria
- Allow users to see all sources (not just top-ranked)
- Explain confidence scores

**Language Diversity:**
- Support non-English sources (via translation)
- Avoid English-language bias
- Include local news outlets

**Implementation:**
```python
def audit_source_diversity(events: List[Event]) -> Dict:
    """Analyze geographic and linguistic diversity of sources."""
    sources_by_region = defaultdict(list)
    languages = defaultdict(int)
    
    for event in events:
        for source in event.sources:
            sources_by_region[source.region].append(source)
            languages[source.language] += 1
    
    return {
        "regional_distribution": dict(sources_by_region),
        "language_distribution": dict(languages),
        "diversity_score": calculate_diversity_index(sources_by_region),
    }
```

### Misuse Prevention

**Rate Limiting:**
- Prevent bulk data scraping
- Monitor for automated access patterns
- Block suspicious IPs

**Terms of Service:**
- Prohibit use for planning attacks
- Prohibit targeting specific individuals/groups
- Reserve right to suspend abusive users

**Monitoring:**
- Track API usage patterns
- Alert on unusual download volumes
- Log all data exports

**Cooperation:**
- Respond to legitimate law enforcement requests
- Publish transparency report (quarterly)
- Work with humanitarian organizations on safety

### Privacy Protection

**Data Minimization:**
- Collect only essential user data
- No location tracking
- No third-party analytics

**GDPR Compliance:**
- Right to access (export all user data)
- Right to deletion (anonymize or delete account)
- Right to portability (machine-readable format)
- Data Processing Agreement with providers

**User Controls:**
- Privacy dashboard
- Download data button
- Delete account button
- Opt-out of non-essential cookies

## Deployment Architecture

### Development

**Local Setup:**
```yaml
# docker-compose.yml
version: '3.8'
services:
  postgres:
    image: postgis/postgis:15-3.3
    environment:
      POSTGRES_DB: wartracker
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
  
  backend:
    build: ./backend
    command: uvicorn app.main:app --reload --host 0.0.0.0
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@postgres/wartracker
      - REDIS_URL=redis://redis:6379
  
  frontend:
    build: ./frontend
    command: npm run dev
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
  
  celery:
    build: ./backend
    command: celery -A app.workers.celery_app worker --loglevel=info
    volumes:
      - ./backend:/app

volumes:
  postgres_data:
```

**Developer Workflow:**
1. `docker-compose up` - Start all services
2. Backend: `http://localhost:8000`
3. Frontend: `http://localhost:3000`
4. API docs: `http://localhost:8000/docs`

### Staging

**Purpose:**
- Pre-production testing
- User acceptance testing
- Performance validation

**Infrastructure:**
- Single backend instance
- Single frontend instance
- Managed PostgreSQL (AWS RDS)
- Managed Redis (AWS ElastiCache)
- Automated deployments from `staging` branch

**URL:** `https://staging.wartracker.org`

### Production

**Architecture:**
```
┌─────────────────────────────────────────────────────┐
│                  Cloudflare CDN                     │
│         (DDoS protection, edge caching)             │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│              Load Balancer (AWS ALB)                │
└─────────────────────────────────────────────────────┘
                        ↓
        ┌───────────────┴───────────────┐
        ↓                               ↓
┌───────────────┐               ┌───────────────┐
│  Frontend 1   │               │  Frontend 2   │
│  (Next.js)    │               │  (Next.js)    │
└───────────────┘               └───────────────┘
        ↓                               ↓
┌───────────────┐               ┌───────────────┐
│  Backend 1    │               │  Backend 2    │
│  (FastAPI)    │               │  (FastAPI)    │
└───────────────┘               └───────────────┘
        ↓                               ↓
        ┌───────────────┴───────────────┐
                        ↓
        ┌───────────────┼───────────────┐
        ↓               ↓               ↓
┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│   PostgreSQL  │ │    Redis      │ │     S3        │
│   (Primary)   │ │   Cluster     │ │  (Assets)     │
│   + Replica   │ │               │ │               │
└───────────────┘ └───────────────┘ └───────────────┘
```

**High Availability:**
- 2+ backend instances (auto-scaling)
- 2+ frontend instances
- PostgreSQL primary + read replica
- Redis Cluster (3 nodes)
- Multi-AZ deployment

**Deployment:**
- GitHub Actions CI/CD
- Blue-green deployment (zero downtime)
- Automated rollback on failure
- Database migrations with Alembic

## Monitoring & Observability

### Logging

**Structured Logging:**
```python
import structlog

logger = structlog.get_logger()

logger.info(
    "event_created",
    event_id=event.id,
    severity=event.severity_score,
    location=event.location,
    source_count=len(event.sources)
)
```

**Log Aggregation:**
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Correlation IDs for request tracing
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Retention: 30 days

### Metrics

**Key Metrics to Track:**

**Performance:**
- API response time (p50, p95, p99)
- Database query time
- Cache hit rate
- WebSocket connection count

**Business:**
- Active conflicts (24h, 7d)
- Events by severity
- Events by region
- Verification rate (% verified)

**User:**
- Daily active users
- Alert creations
- API usage (by tier)
- Export requests

**System:**
- CPU/memory usage
- Disk usage
- Network I/O
- Error rate

**Tools:**
- Prometheus for metrics collection
- Grafana for dashboards
- Custom alerts for anomalies

### Alerting

**Alert Thresholds:**

| Metric | Warning | Critical | Action |
|--------|---------|----------|--------|
| API error rate | > 1% | > 5% | Page on-call |
| Response time p95 | > 500ms | > 2s | Investigate |
| Database connections | > 80% | > 95% | Scale up |
| Cache hit rate | < 70% | < 50% | Investigate |
| Data source failures | ≥ 2 sources | ≥ 3 sources | Check collectors |
| Disk usage | > 70% | > 85% | Clean up / scale |
| Uptime | < 99.5% | < 99% | Incident review |

**Notification Channels:**
- Slack (all alerts)
- PagerDuty (critical only)
- Email (daily summary)

## Open Questions

1. **Data Retention Policy**: How long to store detailed event data vs. aggregated statistics?
   - Proposal: 5 years detailed, indefinite aggregates
   - GDPR consideration: Anonymize after 2 years for EU users

2. **Premium Tier Features**: What features to include in premium tier (future monetization)?
   - Candidates: Higher API limits, advanced analytics, priority support
   - Decision deferred until post-launch

3. **Mobile App Strategy**: Native apps or PWA?
   - Decision: PWA for v1.0, native apps in v2.0 if demand justifies

4. **Additional Data Sources**: Which sources to add post-launch?
   - Priority: Satellite imagery (Maxar), local news APIs
   - Depends on budget and licensing

5. **AI Model Selection**: Which Ollama models for specific tasks?
   - Summarization: qwen3.5:397b-cloud
   - Classification: glm-5:cloud
   - Testing needed to finalize

## Tradeoffs

### 1. Real-time vs. Accuracy
**Decision:** Tiered approach
- Publish immediately with "unverified" badge for high-severity events
- Wait for 2+ sources for moderate events
- Require 3+ sources for low-severity

**Rationale:** Users need timely information, but accuracy is paramount. Transparency about verification status allows users to make informed decisions.

### 2. Coordinate Precision vs. Safety
**Decision:** Blurred coordinates for active high-severity conflicts
- Store precise coordinates in database
- Display blurred coordinates publicly
- Research access with approval

**Rationale:** Safety of civilians and aid workers takes precedence over precision. Researchers can still access precise data with proper oversight.

### 3. Monolith vs. Microservices
**Decision:** Modular monolith for v1.0
- Single codebase, clearly separated modules
- Easy to deploy and maintain
- Can extract services later if needed

**Rationale:** Microservices add complexity without clear benefit at v1.0 scale. Modular design allows future extraction if scaling demands it.

### 4. WebSocket vs. Polling
**Decision:** WebSocket primary, polling fallback
- Real-time updates for connected users
- Graceful degradation to polling
- Minimizes server load

**Rationale:** Real-time is core to value proposition, but must work for all users. Fallback ensures reliability.

### 5. MapLibre vs. Leaflet
**Decision:** MapLibre GL
- Vector tiles (better performance)
- More customizable
- Active development

**Rationale:** Leaflet is simpler but less performant for large datasets. MapLibre better supports our scale and customization needs.

### 6. PostgreSQL vs. MongoDB
**Decision:** PostgreSQL + PostGIS
- ACID compliance
- Mature geospatial support
- Strong consistency

**Rationale:** Data integrity is critical. PostGIS provides excellent geospatial capabilities with relational benefits.

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| v1.0 | 2026-03-01 | Tony | Initial architecture |

---

**Next Phase**: Peter (Developer) will implement based on this architecture.
**Document Location**: `docs/agent-workflow/ARCH.md`
**GitHub**: https://github.com/humac/WarTracker
