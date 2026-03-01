# WarTracker - Issues Log

## Document Purpose
This file tracks ambiguities, technical challenges, ethical concerns, dependencies, and blockers identified during the requirements gathering phase.

---

## Ambiguities

### 1. Data Licensing Uncertainty
**Issue**: ACLED and GDELT have different licensing terms for data redistribution.
- ACLED: Requires attribution, may restrict commercial use
- GDELT: Open license but unclear on derived products
**Impact**: Could limit our ability to display or export certain data
**Resolution Needed**: Legal review before MVP launch
**Status**: ⚠️ OPEN

### 2. Casualty Count Discrepancies
**Issue**: Different sources report conflicting casualty numbers for same event.
**Options**:
- Display range (e.g., "50-100 casualties")
- Show average with confidence interval
- Display all conflicting reports side-by-side
- Flag as "disputed" and show source breakdown
**Impact**: User trust and data accuracy perception
**Resolution Needed**: Tony to design UI pattern for disputed data
**Status**: ⚠️ OPEN

### 3. Geographic Precision vs. Safety
**Issue**: Exact coordinates could endanger civilians, aid workers, or sources in conflict zones.
**Questions**:
- Should we blur coordinates for active conflicts?
- What precision level is safe? (city-level vs. exact location)
- Should users be able to request precise data for research?
**Impact**: Ethical responsibility and user safety
**Resolution Needed**: Ethical review and security policy
**Status**: ⚠️ OPEN

### 4. Real-time vs. Verification Tradeoff
**Issue**: Publishing immediately risks spreading misinformation; waiting risks being outdated.
**Options**:
- Publish immediately with "unverified" badge
- Wait for 2+ sources (5-15 minute delay)
- Tiered approach based on severity
**Impact**: Platform credibility and user trust
**Resolution Needed**: Policy decision on verification thresholds
**Status**: ⚠️ OPEN

### 5. Historical Data Depth
**Issue**: How far back should we go?
- 1 year: Manageable scope, limited context
- 5 years: Better trend analysis, higher storage costs
- 10+ years: Academic value, significant infrastructure needs
**Impact**: Database design, storage costs, user value
**Resolution Needed**: Scope decision based on budget
**Status**: ⚠️ OPEN

---

## Technical Challenges

### 1. Multi-Source Deduplication
**Challenge**: Same conflict event reported by multiple sources with different details.
**Complexity**: High
**Technical Approach**:
- Fuzzy matching on location (geospatial proximity)
- Time window matching (±2 hours)
- Event type classification matching
- Actor name normalization
**Risk**: False positives (merging distinct events) or false negatives (duplicate events)
**Mitigation**: Manual review queue for uncertain matches
**Status**: 📋 IDENTIFIED

### 2. Real-time Data Pipeline
**Challenge**: Ingesting from 5+ sources with ≤5 minute latency.
**Complexity**: High
**Technical Approach**:
- Async data collectors (one per source)
- Redis queue for processing pipeline
- PostgreSQL with materialized views for fast queries
- WebSocket for real-time frontend updates
**Risk**: Bottlenecks during high-volume events
**Mitigation**: Auto-scaling collector services
**Status**: 📋 IDENTIFIED

### 3. Geospatial Query Performance
**Challenge**: Fast queries on 1M+ conflict events with location filters.
**Complexity**: Medium-High
**Technical Approach**:
- PostgreSQL + PostGIS with spatial indexes
- Geohash-based clustering for map tiles
- Query optimization with bounding boxes
**Risk**: Slow map rendering with many markers
**Mitigation**: Server-side clustering, level-of-detail rendering
**Status**: 📋 IDENTIFIED

### 4. Source Credibility Scoring
**Challenge**: Algorithmic assessment of source reliability.
**Complexity**: Medium
**Technical Approach**:
- Historical accuracy tracking
- Editorial transparency scoring
- Cross-source agreement metrics
- Manual tier assignment (Tier 1-4)
**Risk**: Bias in scoring algorithm
**Mitigation**: Transparent methodology, periodic review
**Status**: 📋 IDENTIFIED

### 5. Misinformation Detection
**Challenge**: Identifying false or misleading conflict reports.
**Complexity**: High
**Technical Approach**:
- Single-source flagging
- Contradiction detection (AI/ML)
- Social media bot detection
- User reporting mechanism (future)
**Risk**: False accusations damage credibility
**Mitigation**: Conservative flagging, human review for major claims
**Status**: 📋 IDENTIFIED

### 6. API Rate Limiting & Cost Control
**Challenge**: Balancing data freshness with API costs.
**Complexity**: Medium
**Technical Approach**:
- Intelligent caching (Redis)
- Rate limit per source based on tier
- Cost monitoring dashboard
- Fallback to lower-frequency polling during spikes
**Risk**: Exceeding budget or API limits
**Mitigation**: Daily cost alerts, automatic throttling
**Status**: 📋 IDENTIFIED

---

## Ethical Concerns

### 1. Neutrality & Bias
**Concern**: Perceived or actual bias in conflict coverage.
**Risks**:
- Over-coverage of certain regions (Western media bias)
- Under-coverage of others (Global South)
- Language bias (English-language sources dominate)
**Mitigation**:
- Transparent source list
- Actively diversify data sources
- Regular bias audits
- Clear neutrality disclaimers
**Status**: ⚠️ HIGH PRIORITY

### 2. Harm to Vulnerable Populations
**Concern**: Real-time conflict data could endanger civilians or aid workers.
**Risks**:
- Armed groups monitoring platform
- Targeting of identified locations
- Compromising evacuation routes
**Mitigation**:
- Coordinate blurring for active conflicts
- Time-delayed publishing for sensitive events
- Consultation with humanitarian organizations
- Opt-out mechanism for NGOs
**Status**: ⚠️ HIGH PRIORITY

### 3. Sensationalism & Trauma
**Concern**: Conflict data can be dehumanizing or traumatic.
**Risks**:
- Reducing human suffering to statistics
- Desensitization through constant exposure
- Exploitation for political agendas
**Mitigation**:
- Human-centered design (stories, not just numbers)
- Content warnings for graphic events
- Avoid gamification elements
- Partner with mental health experts on UX
**Status**: ⚠️ MEDIUM PRIORITY

### 4. Surveillance & Privacy
**Concern**: User tracking and data collection.
**Risks**:
- Government requests for user data
- Tracking user interests (could reveal political views)
- Location data from mobile users
**Mitigation**:
- Minimal data collection
- No location tracking
- Transparent privacy policy
- GDPR compliance
- Resist government data requests where legal
**Status**: ⚠️ MEDIUM PRIORITY

### 5. Misuse by Bad Actors
**Concern**: Platform could be used to plan attacks or monitor targets.
**Risks**:
- Terrorist groups using for reconnaissance
- Governments tracking dissidents
- Corporations exploiting conflict zones
**Mitigation**:
- Terms of service prohibiting misuse
- Rate limiting to prevent bulk data scraping
- Monitoring for suspicious usage patterns
- Cooperation with law enforcement on credible threats
**Status**: ⚠️ MEDIUM PRIORITY

---

## Dependencies

### External API Dependencies

| Service | Dependency Level | Fallback Plan | Risk |
|---------|-----------------|---------------|------|
| GDELT | Critical | Manual data entry | Low (stable service) |
| ACLED | Critical | Other conflict databases | Medium (paid tier required) |
| NewsAPI | High | Direct RSS feeds | Low |
| UN OCHA ReliefWeb | Medium | Manual monitoring | Low |
| Twitter/X API | Low | Telegram, other social | Medium (API changes) |
| Telegram | Low | Alternative social monitoring | Low |

### Infrastructure Dependencies

| Service | Dependency Level | Fallback Plan | Risk |
|---------|-----------------|---------------|------|
| PostgreSQL + PostGIS | Critical | Migration to alternative DB | Low |
| Redis | High | In-memory caching alternative | Low |
| Docker | Medium | Direct deployment | Low |
| Ollama Cloud | High | Alternative ML services | Medium |
| Cloud Hosting (AWS/GCP) | Critical | Multi-cloud strategy | Low |

### Human Dependencies

| Role | Dependency | Risk |
|------|------------|------|
| Legal Counsel | Data licensing review | Medium (need external consultant) |
| Ethical Advisor | Conflict sensitivity review | Medium (need expert consultation) |
| Security Auditor | Penetration testing | Low (can hire firm) |
| Humanitarian Partners | Safety guidance | Medium (need to establish relationships) |

---

## Blockers

### Pre-Launch Blockers

1. **Legal Review Required** ⚠️ BLOCKER
   - Data licensing agreements must be reviewed
   - Terms of service must be drafted
   - Privacy policy must be GDPR-compliant
   - **Owner**: Jarvis (coordinator to arrange)
   - **Timeline**: Before public launch

2. **API Access Credentials** ⚠️ BLOCKER
   - ACLED premium API key needed
   - NewsAPI subscription required
   - Budget approval for API costs ($500/month)
   - **Owner**: Jarvis
   - **Timeline**: Before development starts

3. **Ethical Review Board** ⚠️ BLOCKER
   - Consultation with humanitarian organizations
   - Safety impact assessment
   - Coordinate blurring policy
   - **Owner**: Pepper (to coordinate)
   - **Timeline**: Before MVP launch

### Development Blockers

1. **Architecture Decision: Data Model** 📋 PENDING
   - Tony must finalize database schema
   - Depends on: Historical data depth decision
   - **Owner**: Tony
   - **Timeline**: Architecture phase

2. **Architecture Decision: Verification Algorithm** 📋 PENDING
   - Multi-source matching logic
   - Credibility scoring methodology
   - **Owner**: Tony
   - **Timeline**: Architecture phase

3. **Infrastructure: Cloud Provider Selection** 📋 PENDING
   - AWS vs. GCP vs. Azure
   - Cost optimization
   - **Owner**: Jarvis
   - **Timeline**: Before Peter build phase

---

## Risk Register

| Risk | Probability | Impact | Mitigation | Status |
|------|-------------|--------|------------|--------|
| API costs exceed budget | Medium | High | Caching, rate limiting, monitoring | 📋 Monitored |
| Misinformation published | Medium | Critical | Multi-source verification, manual review | ⚠️ Active Mitigation |
| Platform used for harm | Low | Critical | ToS, monitoring, cooperation with authorities | ⚠️ Active Mitigation |
| Data licensing violation | Low | Critical | Legal review, compliance checks | ⚠️ Legal Review Needed |
| Security breach | Low | Critical | Security audits, encryption, best practices | 📋 Planned |
| Low user adoption | Medium | Medium | Marketing, partnerships, UX optimization | 📋 Future Concern |
| Burnout from conflict exposure | Medium | Medium | Team support, content warnings | 📋 Planned |
| Geopolitical pressure/censorship | Low | High | Decentralized hosting, legal protection | 📋 Contingency |

---

## Open Decisions for Tony (Architecture)

1. **Database Schema**: Design for flexibility (unknown future data sources)
2. **Verification Pipeline**: Async processing with retry logic
3. **API Design**: RESTful with clear versioning strategy
4. **Caching Strategy**: Multi-layer (Redis + application-level)
5. **Frontend Architecture**: Component structure for map, filters, alerts
6. **Authentication**: OAuth + email, session management
7. **Deployment**: Docker + Kubernetes or simpler orchestration?

---

## Open Decisions for Pepper (Documentation)

1. **User Guide Tone**: Technical vs. accessible (recommend: accessible)
2. **Admin Guide Depth**: Deployment-only or full operations manual?
3. **Final Report Format**: Narrative or structured template?

---

## Notes for Future Phases

### For Tony (Architecture)
- Prioritize modularity (easy to add new data sources)
- Design for internationalization (even if English-only for v1.0)
- Consider accessibility from the start (not retrofitted)
- Plan for 10x scale from day one

### For Peter (Development)
- Write tests for verification algorithms (critical path)
- Implement feature flags for gradual rollout
- Log everything (debugging will be essential)
- Security-first mindset (input validation, auth)

### For Heimdall (QA)
- Test with realistic data volumes (1M+ events)
- Security audit before any public launch
- Verify neutrality of UI (no implicit bias in design)
- Performance test under load

### For Jarvis (Coordination)
- Arrange legal review ASAP
- Secure API credentials and budget
- Establish ethical advisory relationships
- Plan launch communications

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| v0.1 | 2026-03-01 | Pepper | Initial issues log |

---

**Status**: 📋 Ready for Review  
**Next**: Tony to address technical challenges in architecture phase  
**Location**: `docs/agent-workflow/ISSUES.md`
