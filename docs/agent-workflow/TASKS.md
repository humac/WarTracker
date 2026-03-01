# WarTracker - Implementation Tasks

## Phase 1: Database Setup (4-6 hours)

### TASK-DB-1: Install PostgreSQL + PostGIS
- **Objective**: Set up PostgreSQL 15 with PostGIS extension
- **Files**: 
  - `docker-compose.yml` (create)
  - `backend/alembic/env.py` (configure)
- **Steps**:
  1. Create `docker-compose.yml` with PostgreSQL + PostGIS image
  2. Configure database connection in `backend/.env.example`
  3. Run `docker-compose up -d postgres` to start database
  4. Verify PostGIS extension: `SELECT PostGIS_version();`
- **Tests**: 
  - Connection test script
  - PostGIS extension enabled check
- **Acceptance**: 
  - ✅ PostgreSQL container running
  - ✅ PostGIS extension enabled
  - ✅ Connection string works from backend

### TASK-DB-2: Create Database Schema
- **Objective**: Implement all database tables per ARCH.md schema
- **Files**:
  - `backend/alembic/versions/001_initial_schema.py` (create)
  - `backend/app/models/*.py` (create all models)
- **Tables to Create**:
  - `conflict_events` (with PostGIS geometry)
  - `sources`
  - `verifications`
  - `users`
  - `alerts`
  - `regions`
  - `bookmarks`
  - `user_preferences`
- **Steps**:
  1. Create SQLAlchemy models in `backend/app/models/`
  2. Generate Alembic migration: `alembic revision --autogenerate`
  3. Review and edit migration file
  4. Run migration: `alembic upgrade head`
- **Tests**:
  - Model instantiation tests
  - Relationship tests (foreign keys work)
  - Constraint tests (check constraints enforced)
- **Acceptance**:
  - ✅ All 8 tables created
  - ✅ Foreign key constraints working
  - ✅ Check constraints enforced (severity 1-5, etc.)
  - ✅ PostGIS geometry columns created

### TASK-DB-3: Create Indexes
- **Objective**: Implement all performance indexes per ARCH.md
- **Files**:
  - `backend/alembic/versions/002_add_indexes.py` (create)
- **Indexes to Create**:
  - Geospatial: `idx_conflict_events_location` (GIST)
  - Composite: `idx_conflict_events_active_severity`
  - Temporal: `idx_conflict_events_timestamp`
  - Text search: `idx_conflict_events_title_search` (GIN)
  - And all others from ARCH.md
- **Steps**:
  1. Create index migration file
  2. Add all indexes with correct types (GIST, GIN, B-tree)
  3. Run migration
  4. Verify with `\di` in psql
- **Tests**:
  - Index existence check
  - Query performance test (EXPLAIN ANALYZE)
- **Acceptance**:
  - ✅ All 15+ indexes created
  - ✅ Geospatial queries use GIST index
  - ✅ Text search uses GIN index

### TASK-DB-4: Seed Initial Data
- **Objective**: Populate database with initial sources and regions
- **Files**:
  - `backend/scripts/seed_data.py` (create)
  - `backend/data/sources.json` (create)
  - `backend/data/regions.json` (create)
- **Data to Seed**:
  - 5 primary sources (GDELT, ACLED, NewsAPI, UN OCHA, US State Dept)
  - Source credibility tiers and scores
  - Country regions (all ISO country codes)
- **Steps**:
  1. Create JSON data files
  2. Write seed script using SQLAlchemy
  3. Run seed script: `python scripts/seed_data.py`
  4. Verify data in database
- **Tests**:
  - Seed script idempotency (can run multiple times)
  - Data integrity checks
- **Acceptance**:
  - ✅ 5+ sources seeded with correct tiers
  - ✅ 195 countries in regions table
  - ✅ Seed script can re-run without errors

---

## Phase 2: Backend Core (8-10 hours)

### TASK-BE-1: Set up FastAPI Project Structure
- **Objective**: Create FastAPI application with proper structure
- **Files**:
  - `backend/app/main.py` (create)
  - `backend/app/config.py` (create)
  - `backend/app/database.py` (create)
  - `backend/requirements.txt` (create)
  - `backend/Dockerfile` (create)
- **Steps**:
  1. Create FastAPI app in `main.py`
  2. Configure Pydantic settings in `config.py`
  3. Set up database session in `database.py`
  4. Create requirements.txt with all dependencies
  5. Create Dockerfile for containerization
  6. Test app starts: `uvicorn app.main:app --reload`
- **Tests**:
  - Health check endpoint: `GET /health`
  - Database connection test
- **Acceptance**:
  - ✅ FastAPI app starts without errors
  - ✅ Health endpoint returns 200
  - ✅ Database connection works
  - ✅ Docker build succeeds

### TASK-BE-2: Create Database Models
- **Objective**: Implement all SQLAlchemy models
- **Files**:
  - `backend/app/models/__init__.py` (create)
  - `backend/app/models/conflict_event.py` (create)
  - `backend/app/models/source.py` (create)
  - `backend/app/models/verification.py` (create)
  - `backend/app/models/user.py` (create)
  - `backend/app/models/alert.py` (create)
  - `backend/app/models/region.py` (create)
  - `backend/app/models/bookmark.py` (create)
  - `backend/app/models/user_preference.py` (create)
- **Steps**:
  1. Create each model file per ARCH.md schema
  2. Define relationships (foreign keys, backrefs)
  3. Add validation methods
  4. Import all in `__init__.py`
- **Tests**:
  - Model instantiation tests
  - Relationship tests (e.g., `event.sources` returns list)
  - Cascade delete tests
- **Acceptance**:
  - ✅ All 8 models created
  - ✅ Relationships work correctly
  - ✅ Models match ARCH.md schema exactly

### TASK-BE-3: Implement Data Collectors
- **Objective**: Create async data collectors for each source
- **Files**:
  - `backend/app/collectors/base_collector.py` (create)
  - `backend/app/collectors/gdelt_collector.py` (create)
  - `backend/app/collectors/acled_collector.py` (create)
  - `backend/app/collectors/newsapi_collector.py` (create)
  - `backend/app/collectors/unocha_collector.py` (create)
  - `backend/app/collectors/social_collector.py` (create)
- **Steps**:
  1. Create abstract `BaseCollector` class
  2. Implement `fetch()` and `parse()` for each source
  3. Add rate limiting per source
  4. Add error handling and retry logic
  5. Test each collector individually
- **Tests**:
  - Collector fetch test (mock API responses)
  - Parse test (verify schema compliance)
  - Rate limit test
  - Error handling test (API down)
- **Acceptance**:
  - ✅ 5 collectors implemented
  - ✅ Each collector normalizes to unified schema
  - ✅ Rate limiting works (no API bans)
  - ✅ Error handling graceful (no crashes)

### TASK-BE-4: Build Verification Pipeline
- **Objective**: Implement multi-source verification algorithm
- **Files**:
  - `backend/app/pipelines/normalizer.py` (create)
  - `backend/app/pipelines/deduplication.py` (create)
  - `backend/app/pipelines/verification.py` (create)
  - `backend/app/services/ai_service.py` (create)
- **Steps**:
  1. Implement data normalizer (unified schema)
  2. Implement deduplication (fuzzy matching)
  3. Implement verification algorithm (confidence scoring)
  4. Integrate Ollama for AI classification/summarization
  5. Test pipeline end-to-end
- **Tests**:
  - Normalization test (various source formats)
  - Deduplication test (same event from multiple sources)
  - Verification test (confidence score calculation)
  - AI service test (mock Ollama)
- **Acceptance**:
  - ✅ Pipeline processes events correctly
  - ✅ Duplicates detected and merged
  - ✅ Confidence scores calculated per formula
  - ✅ AI summaries generated

### TASK-BE-5: Create API Endpoints
- **Objective**: Implement all RESTful API endpoints per ARCH.md
- **Files**:
  - `backend/app/api/v1/events.py` (create)
  - `backend/app/api/v1/sources.py` (create)
  - `backend/app/api/v1/alerts.py` (create)
  - `backend/app/api/v1/users.py` (create)
  - `backend/app/api/v1/regions.py` (create)
  - `backend/app/api/v1/export.py` (create)
  - `backend/app/api/deps.py` (create)
- **Endpoints to Implement**:
  - Authentication: register, login, OAuth, refresh, logout, me
  - Events: list, get, nearby, timeline, stats
  - Alerts: CRUD, test
  - Users: profile, preferences, bookmarks
  - Export: CSV, JSON, RSS
- **Steps**:
  1. Create API routers per resource
  2. Implement authentication dependencies
  3. Add request/response schemas (Pydantic)
  4. Implement business logic in services
  5. Add OpenAPI documentation
- **Tests**:
  - Endpoint tests (all HTTP methods)
  - Authentication tests (valid/invalid tokens)
  - Validation tests (invalid input)
  - Integration tests (full request flow)
- **Acceptance**:
  - ✅ All 25+ endpoints implemented
  - ✅ OpenAPI docs at `/docs` complete
  - ✅ Authentication working (JWT + OAuth)
  - ✅ Rate limiting enforced

### TASK-BE-6: Implement Caching Layer
- **Objective**: Set up Redis caching with multi-layer strategy
- **Files**:
  - `backend/app/utils/cache.py` (create)
  - `backend/app/services/cache_service.py` (create)
- **Steps**:
  1. Configure Redis connection
  2. Implement cache decorators for endpoints
  3. Implement cache invalidation logic
  4. Add cache warming on data updates
  5. Test cache hit/miss behavior
- **Tests**:
  - Cache hit test (second request faster)
  - Cache invalidation test (update clears cache)
  - TTL test (cache expires)
- **Acceptance**:
  - ✅ Redis connected and working
  - ✅ Cache decorators functional
  - ✅ Cache hit rate > 70% under load
  - ✅ Invalidation works on writes

---

## Phase 3: Frontend Core (8-10 hours)

### TASK-FE-1: Set up Next.js Project
- **Objective**: Initialize Next.js 16 project with App Router
- **Files**:
  - `frontend/package.json` (create)
  - `frontend/next.config.js` (create)
  - `frontend/tsconfig.json` (create)
  - `frontend/tailwind.config.js` (create)
  - `frontend/app/layout.tsx` (create)
  - `frontend/app/page.tsx` (create)
  - `frontend/app/globals.css` (create)
  - `frontend/Dockerfile` (create)
- **Steps**:
  1. Initialize Next.js project: `npx create-next-app@latest`
  2. Configure TypeScript
  3. Configure Tailwind CSS
  4. Set up App Router structure
  5. Create Dockerfile
  6. Test dev server: `npm run dev`
- **Tests**:
  - Build test: `npm run build`
  - Lint test: `npm run lint`
- **Acceptance**:
  - ✅ Next.js app starts without errors
  - ✅ TypeScript compiles
  - ✅ Tailwind styles working
  - ✅ Docker build succeeds

### TASK-FE-2: Create Base Components
- **Objective**: Build reusable UI component library
- **Files**:
  - `frontend/components/ui/button.tsx` (create)
  - `frontend/components/ui/card.tsx` (create)
  - `frontend/components/ui/dialog.tsx` (create)
  - `frontend/components/ui/input.tsx` (create)
  - `frontend/components/ui/select.tsx` (create)
  - `frontend/components/ui/badge.tsx` (create)
  - `frontend/components/ui/spinner.tsx` (create)
- **Steps**:
  1. Create each component with TypeScript
  2. Add Tailwind styling
  3. Support dark mode
  4. Add Storybook stories (optional)
- **Tests**:
  - Component render tests
  - Interaction tests (click, type)
  - Accessibility tests (ARIA labels)
- **Acceptance**:
  - ✅ 10+ base components created
  - ✅ All components support dark mode
  - ✅ Components accessible (screen reader friendly)

### TASK-FE-3: Implement Interactive Map
- **Objective**: Build MapLibre GL integration with conflict markers
- **Files**:
  - `frontend/components/map/conflict-map.tsx` (create)
  - `frontend/components/map/event-marker.tsx` (create)
  - `frontend/components/map/marker-cluster.tsx` (create)
  - `frontend/components/map/map-controls.tsx` (create)
  - `frontend/components/map/map-legend.tsx` (create)
  - `frontend/lib/map-utils.ts` (create)
- **Steps**:
  1. Install MapLibre GL: `npm install maplibre-gl`
  2. Create map component with proper initialization
  3. Implement marker rendering (color-coded by severity)
  4. Add clustering for dense areas
  5. Add map controls (zoom, filter)
  6. Add legend showing severity colors
- **Tests**:
  - Map renders without errors
  - Markers appear at correct coordinates
  - Clustering works at low zoom
  - Click on marker shows popup
- **Acceptance**:
  - ✅ Map loads in ≤3 seconds
  - ✅ 100+ markers render smoothly
  - ✅ Clustering works correctly
  - ✅ Severity colors match spec (green→red)

### TASK-FE-4: Build Conflict Event Display
- **Objective**: Create event detail panels and lists
- **Files**:
  - `frontend/components/events/event-card.tsx` (create)
  - `frontend/components/events/event-detail.tsx` (create)
  - `frontend/components/events/event-list.tsx` (create)
  - `frontend/components/events/event-timeline.tsx` (create)
  - `frontend/components/events/source-list.tsx` (create)
  - `frontend/hooks/use-events.ts` (create)
- **Steps**:
  1. Create event card component (summary view)
  2. Create event detail panel (full view)
  3. Create event list (sidebar view)
  4. Create timeline visualization
  5. Create source list with verification badges
  6. Implement React Query hooks for data fetching
- **Tests**:
  - Event data displays correctly
  - Verification badges show correct status
  - Timeline renders events chronologically
  - Source list shows all sources
- **Acceptance**:
  - ✅ Event cards show all required info
  - ✅ Verification badges (✓ Verified, ⚠ Unverified, ⚡ Developing)
  - ✅ Source list with clickable links
  - ✅ Timeline view functional

### TASK-FE-5: Create User Authentication UI
- **Objective**: Build login, register, and OAuth flows
- **Files**:
  - `frontend/app/(auth)/login/page.tsx` (create)
  - `frontend/app/(auth)/register/page.tsx` (create)
  - `frontend/app/(auth)/oauth/callback/route.tsx` (create)
  - `frontend/context/auth-context.tsx` (create)
  - `frontend/hooks/use-auth.ts` (create)
  - `frontend/components/layout/header.tsx` (create)
- **Steps**:
  1. Create login form with validation
  2. Create registration form
  3. Implement OAuth buttons (Google, GitHub)
  4. Create auth context for state management
  5. Add protected route logic
  6. Implement logout functionality
- **Tests**:
  - Login form validation
  - Registration flow
  - OAuth callback handling
  - Protected route redirects
- **Acceptance**:
  - ✅ Login/register forms work
  - ✅ OAuth login functional
  - ✅ Auth state persists (refresh token)
  - ✅ Protected routes redirect to login

### TASK-FE-6: Implement Alert System UI
- **Objective**: Build alert creation and management interface
- **Files**:
  - `frontend/app/(dashboard)/alerts/page.tsx` (create)
  - `frontend/app/(dashboard)/alerts/create/page.tsx` (create)
  - `frontend/components/alerts/alert-form.tsx` (create)
  - `frontend/components/alerts/alert-list.tsx` (create)
  - `frontend/components/alerts/alert-card.tsx` (create)
  - `frontend/hooks/use-alerts.ts` (create)
- **Steps**:
  1. Create alert list page
  2. Create alert creation form (region, type, severity)
  3. Create alert card component
  4. Implement CRUD operations
  5. Add alert test functionality
  6. Add notification preferences
- **Tests**:
  - Alert creation form validation
  - Alert list displays correctly
  - Alert update/delete works
  - Test alert sends notification
- **Acceptance**:
  - ✅ Users can create alerts
  - ✅ Alert filters work (region, type, severity)
  - ✅ Alert list shows all user alerts
  - ✅ Test alert button functional

---

## Phase 4: Integration (6-8 hours)

### TASK-INT-1: Connect Frontend to Backend
- **Objective**: Integrate frontend with backend API
- **Files**:
  - `frontend/lib/api.ts` (create)
  - `frontend/.env.local.example` (create)
- **Steps**:
  1. Create API client (axios/fetch wrapper)
  2. Configure base URL and interceptors
  3. Add authentication token handling
  4. Test all API endpoints from frontend
  5. Handle API errors gracefully
- **Tests**:
  - API client fetches events
  - Auth token included in requests
  - Error handling (401, 403, 500)
- **Acceptance**:
  - ✅ Frontend successfully calls backend
  - ✅ Auth tokens sent with requests
  - ✅ Errors handled with user-friendly messages

### TASK-INT-2: Implement Real-time Updates
- **Objective**: Set up WebSocket for live event updates
- **Files**:
  - `frontend/lib/websocket.ts` (create)
  - `frontend/hooks/use-websocket.ts` (create)
  - `backend/app/api/v1/websocket.py` (create)
- **Steps**:
  1. Set up WebSocket endpoint in backend
  2. Create WebSocket client in frontend
  3. Implement event handlers (NEW_EVENT, EVENT_UPDATED, etc.)
  4. Add reconnection logic
  5. Add fallback to polling if WebSocket unavailable
  6. Test real-time updates
- **Tests**:
  - WebSocket connects successfully
  - New events appear without refresh
  - Reconnection works after disconnect
  - Fallback to polling works
- **Acceptance**:
  - ✅ WebSocket connection stable
  - ✅ New events appear in real-time
  - ✅ Notifications show for new events
  - ✅ Fallback to polling functional

### TASK-INT-3: Test Data Flow End-to-End
- **Objective**: Verify complete data pipeline
- **Files**:
  - `backend/tests/test_e2e.py` (create)
  - `frontend/tests/e2e.test.ts` (create)
- **Steps**:
  1. Seed test data in database
  2. Run data collectors (mock or real)
  3. Verify events appear in API
  4. Verify events display on map
  5. Verify real-time updates work
  6. Test full user journey
- **Tests**:
  - E2E test: Data source → API → Map
  - User journey test: Login → Create alert → Receive notification
- **Acceptance**:
  - ✅ Data flows from source to map
  - ✅ Verification pipeline works
  - ✅ Real-time updates functional
  - ✅ User alerts trigger correctly

### TASK-INT-4: Performance Optimization
- **Objective**: Optimize application performance
- **Files**:
  - Various (optimization throughout codebase)
- **Steps**:
  1. Run Lighthouse audit on frontend
  2. Profile backend API response times
  3. Optimize slow database queries
  4. Implement code splitting in frontend
  5. Optimize images and assets
  6. Test under load (100 concurrent users)
- **Tests**:
  - Lighthouse score > 90
  - API p95 response time < 500ms
  - Map load time < 3 seconds
- **Acceptance**:
  - ✅ Lighthouse score ≥ 90
  - ✅ API p95 < 500ms
  - ✅ Map loads in ≤3 seconds
  - ✅ No memory leaks

---

## Phase 5: Testing & QA (4-6 hours)

### TASK-TEST-1: Write Unit Tests
- **Objective**: Achieve ≥80% code coverage
- **Files**:
  - `backend/tests/test_*.py` (create all test files)
  - `frontend/tests/**/*.test.ts` (create all test files)
- **Steps**:
  1. Write unit tests for all backend services
  2. Write unit tests for all frontend components
  3. Write unit tests for utilities
  4. Run test suite: `pytest` and `npm test`
  5. Fix failing tests
  6. Generate coverage report
- **Tests**:
  - Backend: pytest with coverage
  - Frontend: Jest/Vitest with coverage
- **Acceptance**:
  - ✅ Backend coverage ≥ 80%
  - ✅ Frontend coverage ≥ 80%
  - ✅ All tests passing

### TASK-TEST-2: Write Integration Tests
- **Objective**: Test component interactions
- **Files**:
  - `backend/tests/integration/` (create)
  - `frontend/tests/integration/` (create)
- **Steps**:
  1. Test API endpoint integrations
  2. Test database integrations
  3. Test cache integrations
  4. Test frontend-backend integration
  5. Test WebSocket integration
- **Tests**:
  - API integration tests
  - Database integration tests
  - End-to-end flow tests
- **Acceptance**:
  - ✅ All integration tests passing
  - ✅ API endpoints work together correctly
  - ✅ Data consistency verified

### TASK-TEST-3: Security Audit
- **Objective**: Identify and fix security vulnerabilities
- **Files**:
  - `docs/SECURITY_AUDIT.md` (create)
- **Steps**:
  1. Run automated security scan (bandit, npm audit)
  2. Manual code review for vulnerabilities
  3. Test authentication bypass attempts
  4. Test SQL injection attempts
  5. Test XSS vulnerabilities
  6. Test rate limiting effectiveness
  7. Document findings and fixes
- **Tests**:
  - Security scanner results
  - Penetration test results
- **Acceptance**:
  - ✅ No critical/high vulnerabilities
  - ✅ Authentication secure
  - ✅ Input validation working
  - ✅ Rate limiting effective

### TASK-TEST-4: Performance Testing
- **Objective**: Verify performance under load
- **Files**:
  - `backend/tests/performance/` (create)
  - `docs/PERFORMANCE_REPORT.md` (create)
- **Steps**:
  1. Set up load testing tool (locust, k6)
  2. Create load test scenarios
  3. Test with 100 concurrent users
  4. Test with 1000 concurrent users
  5. Monitor system resources
  6. Identify bottlenecks
  7. Document results
- **Tests**:
  - Load test: 100 concurrent users
  - Load test: 1000 concurrent users
  - Stress test: Breaking point
- **Acceptance**:
  - ✅ 100 concurrent users: response time ≤ 2s
  - ✅ 1000 concurrent users: no crashes
  - ✅ Database query time ≤ 500ms
  - ✅ Cache hit rate ≥ 70%

---

## Task Dependencies

```
Phase 1 (Database)
├── TASK-DB-1 → TASK-DB-2 → TASK-DB-3 → TASK-DB-4
│
Phase 2 (Backend)
├── TASK-BE-1 → TASK-BE-2 → TASK-BE-3
│                        → TASK-BE-4
│                        → TASK-BE-5
│                        → TASK-BE-6
│
Phase 3 (Frontend)
├── TASK-FE-1 → TASK-FE-2 → TASK-FE-3
│                        → TASK-FE-4
│                        → TASK-FE-5
│                        → TASK-FE-6
│
Phase 4 (Integration)
├── TASK-INT-1 (requires Phase 2 + 3 complete)
├── TASK-INT-2 (requires TASK-INT-1)
├── TASK-INT-3 (requires TASK-INT-2)
└── TASK-INT-4 (requires TASK-INT-3)
│
Phase 5 (Testing)
├── TASK-TEST-1 (parallel with Phase 2-4)
├── TASK-TEST-2 (requires TASK-TEST-1)
├── TASK-TEST-3 (requires Phase 4 complete)
└── TASK-TEST-4 (requires Phase 4 complete)
```

---

## Estimated Hours Summary

| Phase | Tasks | Estimated Hours |
|-------|-------|----------------|
| Phase 1: Database | 4 tasks | 4-6 hours |
| Phase 2: Backend | 6 tasks | 8-10 hours |
| Phase 3: Frontend | 6 tasks | 8-10 hours |
| Phase 4: Integration | 4 tasks | 6-8 hours |
| Phase 5: Testing | 4 tasks | 4-6 hours |
| **Total** | **24 tasks** | **30-40 hours** |

---

## Definition of Done

A task is considered complete when:
- [ ] Code implemented per specification
- [ ] Tests written and passing
- [ ] Code reviewed (if applicable)
- [ ] Documentation updated
- [ ] No linting errors
- [ ] Acceptance criteria met

---

## Notes for Peter

1. **Start with Phase 1** - Database foundation is critical
2. **Use Docker** - Ensures consistent environment
3. **Write tests as you go** - Don't defer testing
4. **Check ARCH.md frequently** - Reference for all decisions
5. **Ask if unclear** - Better to ask than assume
6. **Commit frequently** - Small, atomic commits
7. **Verify in browser** - Don't trust code alone, check runtime

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| v1.0 | 2026-03-01 | Tony | Initial task breakdown |

---

**Next**: Peter implements features per these tasks.
**Document Location**: `docs/agent-workflow/TASKS.md`
**GitHub**: https://github.com/humac/WarTracker
