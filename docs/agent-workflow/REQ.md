# WarTracker - Requirements Document

## Version
v0.1 (Initial Requirements)

## Mission Statement
WarTracker provides real-time, verified information on global conflicts by continuously monitoring multiple data sources, cross-referencing reports to combat misinformation, and delivering actionable intelligence through an interactive map and customizable alerts—empowering journalists, researchers, and concerned citizens with accurate, timely conflict data while maintaining strict neutrality and ethical reporting standards.

## Target Users

### Primary Personas

**1. Investigative Journalist (Sarah, 34)**
- Works for international news outlet
- Needs: Real-time conflict alerts, source verification, historical context
- Pain points: Misinformation overload, slow verification processes, fragmented sources
- Technical level: Advanced

**2. Academic Researcher (Dr. Chen, 52)**
- Political science professor studying conflict patterns
- Needs: Historical data exports, trend analysis, API access for research
- Pain points: Data inconsistency, lack of standardized conflict metrics
- Technical level: Intermediate

**3. NGO Humanitarian Worker (Amira, 29)**
- Coordinates aid deployment in conflict zones
- Needs: Real-time severity maps, evacuation alerts, reliable source verification
- Pain points: Safety risks from outdated information, difficulty assessing conflict intensity
- Technical level: Basic to Intermediate

**4. Policy Analyst (Marcus, 41)**
- Works for government think tank
- Needs: Trend analysis, escalation warnings, multi-source verification
- Pain points: Information silos, delayed reporting, bias in sources
- Technical level: Advanced

**5. Concerned Citizen (Alex, 26)**
- Follows global events, shares on social media
- Needs: Simple map view, clear severity indicators, reliable summaries
- Pain points: Conflicting news reports, information overload, sensationalism
- Technical level: Basic

### Secondary Personas

**6. Data Journalist** - Needs API access, bulk data exports
**7. Insurance Risk Analyst** - Needs regional stability metrics
**8. Corporate Security Manager** - Needs travel safety alerts
**9. Student/Graduate Researcher** - Needs accessible historical data
**10. International Organization Staff** - Needs coordinated situational awareness

## User Stories

### High Priority (MVP)

- [ ] **US-1**: As an investigative journalist, I want real-time alerts for conflicts in specific regions so that I can respond quickly to breaking events.
- [ ] **US-2**: As a researcher, I want to view conflicts on an interactive map with severity indicators so that I can understand geographic patterns.
- [ ] **US-3**: As an NGO worker, I want multi-source verification badges on conflict reports so that I can trust the information before acting on it.
- [ ] **US-4**: As a policy analyst, I want to filter conflicts by type (armed conflict, protests, terrorism) so that I can focus on relevant events.
- [ ] **US-5**: As a concerned citizen, I want a simple dashboard showing current global hotspots so that I can stay informed without information overload.
- [ ] **US-6**: As any user, I want to see the source list for each conflict event so that I can evaluate credibility myself.
- [ ] **US-7**: As a journalist, I want historical timeline views for ongoing conflicts so that I can understand escalation patterns.
- [ ] **US-8**: As a researcher, I want to export conflict data in CSV/JSON format so that I can perform my own analysis.
- [ ] **US-9**: As an NGO worker, I want customizable alert thresholds (e.g., only severe conflicts) so that I'm not overwhelmed by notifications.
- [ ] **US-10**: As any user, I want clear neutrality disclaimers on all data so that I understand WarTracker doesn't take political positions.

### Medium Priority (v1.0)

- [ ] **US-11**: As a data journalist, I want API access to conflict data so that I can integrate it into my own applications.
- [ ] **US-12**: As a researcher, I want advanced search filters (date range, casualty counts, actors involved) so that I can find specific events.
- [ ] **US-13**: As a policy analyst, I want AI-generated trend summaries so that I can quickly understand emerging patterns.
- [ ] **US-14**: As an NGO worker, I want offline map downloads for field use so that I can access data without internet.
- [ ] **US-15**: As a concerned citizen, I want email digest summaries (daily/weekly) so that I can stay informed without constant monitoring.
- [ ] **US-16**: As any user, I want to save/bookmark specific conflicts for tracking so that I can follow developing situations.
- [ ] **US-17**: As a researcher, I want comparison views (side-by-side conflict metrics) so that I can analyze multiple regions.
- [ ] **US-18**: As a journalist, I want source credibility scores so that I can prioritize high-reliability reports.
- [ ] **US-19**: As any user, I want mobile-responsive design so that I can access WarTracker on phones and tablets.
- [ ] **US-20**: As an academic, I want citation-ready event data (timestamps, source URLs) so that I can reference in publications.

### Low Priority (Future)

- [ ] **US-21**: As a corporate security manager, I want travel safety risk scores for specific countries so that I can advise employees.
- [ ] **US-22**: As an insurance analyst, I want predictive risk models for regional stability so that I can assess long-term risks.
- [ ] **US-23**: As a user, I want personalized feeds based on my interests so that I see relevant conflicts first.
- [ ] **US-24**: As a researcher, I want integration with academic databases (JSTOR, Google Scholar) so that I can cross-reference with published research.
- [ ] **US-25**: As an NGO, I want collaborative annotation features so that field teams can add ground-truth observations.
- [ ] **US-26**: As a journalist, I want secure, encrypted communication channels for sensitive sources so that I can protect whistleblowers.
- [ ] **US-27**: As any user, I want social media sharing with auto-generated infographics so that I can spread awareness.
- [ ] **US-28**: As a student, I want educational mode with guided tutorials on conflict analysis so that I can learn methodology.
- [ ] **US-29**: As a developer, I want webhook integrations so that I can trigger automated workflows.
- [ ] **US-30**: As any user, I want dark mode and accessibility features (screen reader support) so that the platform is inclusive.

## Functional Requirements

### Data Collection

- [ ] **FR-DATA-1**: System shall ingest data from minimum 5 primary sources (GDELT, ACLED, NewsAPI, UN OCHA, ReliefWeb) via API or RSS feeds.
- [ ] **FR-DATA-2**: System shall parse and normalize conflict event data into standardized schema (event type, location, actors, casualties, timestamp, sources).
- [ ] **FR-DATA-3**: System shall extract geolocation data (latitude/longitude) from all conflict reports with ≥95% accuracy.
- [ ] **FR-DATA-4**: System shall collect social media mentions (Twitter/X, Telegram public channels) for cross-referencing major events.
- [ ] **FR-DATA-5**: System shall ingest government reports (US State Department, UK FCO) for official conflict assessments.
- [ ] **FR-DATA-6**: System shall support manual data entry for verified events not captured by automated sources.
- [ ] **FR-DATA-7**: System shall tag each event with source metadata (source name, URL, timestamp, credibility score).
- [ ] **FR-DATA-8**: System shall deduplicate events from multiple sources reporting same incident (fuzzy matching on location, time, event type).

### Data Processing

- [ ] **FR-PROC-1**: System shall assign severity scores (1-5) to each conflict based on casualty counts, escalation indicators, and geographic spread.
- [ ] **FR-PROC-2**: System shall cross-reference events across minimum 3 independent sources before marking as "verified".
- [ ] **FR-PROC-3**: System shall calculate source credibility scores based on historical accuracy, transparency, and editorial standards.
- [ ] **FR-PROC-4**: System shall detect emerging conflict patterns using AI/ML models (escalation trends, actor behavior, geographic clustering).
- [ ] **FR-PROC-5**: System shall generate automatic summaries for each conflict event (2-3 sentence overview).
- [ ] **FR-PROC-6**: System shall classify conflict types (armed conflict, civil unrest, terrorism, humanitarian crisis, natural disaster) with ≥90% accuracy.
- [ ] **FR-PROC-7**: System shall maintain historical event timeline with ability to query by date range.
- [ ] **FR-PROC-8**: System shall flag potential misinformation events (single-source reports, unverified social media claims, contradictory reports).

### User Interface

- [ ] **FR-UI-1**: System shall display interactive world map with conflict markers color-coded by severity (green=1, yellow=2, orange=3, red=4, dark red=5).
- [ ] **FR-UI-2**: System shall provide clickable conflict markers that open detail panels with event information, sources, and timeline.
- [ ] **FR-UI-3**: System shall offer filter controls for conflict type, severity, date range, and geographic region.
- [ ] **FR-UI-4**: System shall display dashboard with key metrics (active conflicts, 24h changes, trending regions).
- [ ] **FR-UI-5**: System shall provide search functionality with autocomplete for country/region names.
- [ ] **FR-UI-6**: System shall show source list for each event with clickable links to original reports.
- [ ] **FR-UI-7**: System shall display verification badges (✓ Verified, ⚠ Unverified, ⚡ Developing) on event cards.
- [ ] **FR-UI-8**: System shall offer timeline view showing conflict evolution over selectable time periods.
- [ ] **FR-UI-9**: System shall provide data export buttons (CSV, JSON) for filtered result sets.
- [ ] **FR-UI-10**: System shall be fully responsive on mobile devices (≥320px width) and tablets.
- [ ] **FR-UI-11**: System shall display neutrality disclaimer on all pages and in footer.
- [ ] **FR-UI-12**: System shall offer dark mode toggle for user preference.

### Alerts & Notifications

- [ ] **FR-ALERT-1**: System shall allow users to create custom alerts by region, conflict type, and severity threshold.
- [ ] **FR-ALERT-2**: System shall send real-time push notifications (web) for high-severity (4-5) conflicts in watched regions.
- [ ] **FR-ALERT-3**: System shall support email notifications with configurable frequency (instant, daily digest, weekly digest).
- [ ] **FR-ALERT-4**: System shall allow users to set alert quiet hours to avoid notifications during specified times.
- [ ] **FR-ALERT-5**: System shall provide alert management dashboard (create, edit, pause, delete alerts).
- [ ] **FR-ALERT-6**: System shall escalate notifications for rapidly escalating conflicts (severity increase ≥2 levels in 24h).
- [ ] **FR-ALERT-7**: System shall support RSS feed subscriptions for filtered conflict data.

### User Management

- [ ] **FR-USER-1**: System shall support guest access (no authentication required) for basic map viewing and public data.
- [ ] **FR-USER-2**: System shall support user registration with email verification for personalized features.
- [ ] **FR-USER-3**: System shall support OAuth login (Google, GitHub) for streamlined authentication.
- [ ] **FR-USER-4**: System shall allow users to save bookmarks/favorites for tracking specific conflicts.
- [ ] **FR-USER-5**: System shall store user alert preferences and notification history.
- [ ] **FR-USER-6**: System shall provide account settings for notification preferences, export formats, and display options.
- [ ] **FR-USER-7**: System shall support role-based access (free tier, premium tier for advanced features like API access).

### API & Integration

- [ ] **FR-API-1**: System shall provide RESTful API for programmatic access to conflict data.
- [ ] **FR-API-2**: System shall support API authentication via API keys for registered users.
- [ ] **FR-API-3**: System shall implement rate limiting (100 requests/hour for free tier, 1000/hour for premium).
- [ ] **FR-API-4**: System shall provide API documentation with example queries and response schemas.
- [ ] **FR-API-5**: System shall support webhook callbacks for real-time event notifications.

## Non-Functional Requirements

### Performance

- [ ] **NFR-PERF-1**: System shall load initial map view in ≤3 seconds on broadband connection (≥25 Mbps).
- [ ] **NFR-PERF-2**: System shall update conflict data every 5 minutes for high-severity events, every 30 minutes for moderate events.
- [ ] **NFR-PERF-3**: System shall support 10,000 concurrent users without degradation (response time ≤2 seconds).
- [ ] **NFR-PERF-4**: System shall handle 1 million conflict events in database with query response ≤500ms.
- [ ] **NFR-PERF-5**: System shall achieve 99.5% uptime (≤4 hours downtime/month).
- [ ] **NFR-PERF-6**: System shall cache frequently accessed data to reduce API calls to external sources by ≥80%.

### Security

- [ ] **NFR-SEC-1**: System shall encrypt all data in transit using TLS 1.3.
- [ ] **NFR-SEC-2**: System shall encrypt sensitive data at rest (user credentials, API keys) using AES-256.
- [ ] **NFR-SEC-3**: System shall implement rate limiting and DDoS protection on all public endpoints.
- [ ] **NFR-SEC-4**: System shall sanitize all user inputs to prevent XSS and SQL injection attacks.
- [ ] **NFR-SEC-5**: System shall conduct quarterly security audits and penetration testing.
- [ ] **NFR-SEC-6**: System shall comply with GDPR for EU users (data portability, right to deletion).
- [ ] **NFR-SEC-7**: System shall log all authentication attempts and alert on suspicious activity.
- [ ] **NFR-SEC-8**: System shall implement Content Security Policy (CSP) headers to prevent code injection.

### Reliability

- [ ] **NFR-REL-1**: System shall implement automatic failover for database (primary/replica PostgreSQL cluster).
- [ ] **NFR-REL-2**: System shall queue data ingestion tasks with retry logic (3 retries with exponential backoff).
- [ ] **NFR-REL-3**: System shall monitor all data sources and alert administrators if ≥2 sources fail simultaneously.
- [ ] **NFR-REL-4**: System shall maintain data integrity with transactional consistency (ACID compliance).
- [ ] **NFR-REL-5**: System shall perform daily automated backups with 30-day retention.
- [ ] **NFR-REL-6**: System shall provide graceful degradation (read-only mode) if write operations fail.

### Scalability

- [ ] **NFR-SCALE-1**: System shall support horizontal scaling of backend services (containerized deployment).
- [ ] **NFR-SCALE-2**: System shall handle 10x traffic spikes during major global events without manual intervention.
- [ ] **NFR-SCALE-3**: System shall support geographic distribution (CDN for static assets, regional database replicas).

### Accessibility

- [ ] **NFR-ACC-1**: System shall comply with WCAG 2.1 AA standards for accessibility.
- [ ] **NFR-ACC-2**: System shall support screen readers with proper ARIA labels on all interactive elements.
- [ ] **NFR-ACC-3**: System shall provide keyboard navigation for all features (no mouse required).
- [ ] **NFR-ACC-4**: System shall support colorblind users with non-color-dependent severity indicators (icons + colors).

### Maintainability

- [ ] **NFR-MAINT-1**: System shall achieve ≥80% code coverage with automated unit tests.
- [ ] **NFR-MAINT-2**: System shall document all public APIs with OpenAPI/Swagger specification.
- [ ] **NFR-MAINT-3**: System shall implement structured logging with correlation IDs for debugging.
- [ ] **NFR-MAINT-4**: System shall support zero-downtime deployments (blue-green or rolling updates).

## Data Sources

### Primary Sources

1. **GDELT Project** - Global event database with conflict codes - API (gdeltdb.com)
2. **ACLED (Armed Conflict Location & Event Data)** - Real-time conflict event data - API (acleddata.com)
3. **NewsAPI** - Aggregated news articles from 80,000+ sources - REST API (newsapi.org)
4. **UN OCHA ReliefWeb** - Humanitarian crisis reports - RSS/API (reliefweb.int)
5. **US State Department Travel Advisories** - Official government conflict assessments - RSS Feed

### Secondary Sources

1. **ReliefWeb** - Humanitarian situation reports - RSS/API
2. **International Crisis Group** - Conflict analysis reports - RSS Feed
3. **Human Rights Watch** - Human rights violation reports - RSS Feed
4. **BBC Monitoring** - International media monitoring - API (subscription)
5. **Reuters News API** - Global news wire service - REST API (subscription)
6. **Twitter/X API** - Social media monitoring for real-time events - API v2
7. **Telegram Public Channels** - Regional conflict monitoring - MTProto API
8. **Institute for the Study of War** - Military conflict analysis - RSS Feed
9. **European External Programme with Africa (EEPA)** - African conflict monitoring - RSS Feed
10. **Satellite Imagery (Maxar, Planet Labs)** - Visual verification of conflict zones - API (subscription)

### Source Credibility Framework

| Tier | Sources | Verification Requirement |
|------|---------|-------------------------|
| Tier 1 (Highest) | ACLED, GDELT, UN OCHA, Government sources | Auto-verified |
| Tier 2 (High) | Major news wires (Reuters, AP), established NGOs | 2+ sources |
| Tier 3 (Medium) | Regional news outlets, smaller NGOs | 3+ sources |
| Tier 4 (Low) | Social media, blogs, citizen journalists | 5+ sources + manual review |

## Acceptance Criteria

### MVP Definition

WarTracker v1.0 is complete when:

- [ ] **AC-1**: Interactive map displays ≥100 active conflict events with accurate geolocation
- [ ] **AC-2**: System ingests data from minimum 5 primary sources with ≤5 minute latency
- [ ] **AC-3**: Multi-source verification system correctly identifies ≥90% of verified events (validated against manual review)
- [ ] **AC-4**: Users can create and receive alerts for specific regions with ≤1 minute notification delay
- [ ] **AC-5**: Map loads in ≤3 seconds on standard broadband connection (tested on 3 devices)
- [ ] **AC-6**: System achieves ≥99.5% uptime over 30-day testing period
- [ ] **AC-7**: All user stories US-1 through US-10 are functional and tested
- [ ] **AC-8**: Security audit passes with no critical or high-severity vulnerabilities
- [ ] **AC-9**: API documentation is complete and functional (all endpoints tested)
- [ ] **AC-10**: Mobile-responsive design verified on ≥3 device sizes (phone, tablet, desktop)

## Out of Scope (v1.0)

- [ ] Mobile native applications (iOS/Android) - web-responsive only for v1.0
- [ ] User-submitted reports/crowdsourcing - too high risk for misinformation
- [ ] Predictive conflict modeling - requires extensive ML training data
- [ ] Satellite imagery integration - cost prohibitive for MVP
- [ ] Paid premium tier - free tier only for initial launch
- [ ] Multi-language support - English only for v1.0
- [ ] Offline mode - requires significant architecture changes
- [ ] Social media auto-posting - ethical concerns about conflict sensationalism
- [ ] Integration with academic databases - lower priority than core features
- [ ] Encrypted communication channels - scope creep, focus on core monitoring

## Open Questions

1. **Data Licensing**: What are the licensing restrictions for redistributing ACLED/GDELT data? Need legal review before launch.
2. **Casualty Count Verification**: How to handle conflicting casualty reports from different sources? (average, range, or flag as disputed?)
3. **Real-time vs. Accuracy Tradeoff**: Should we delay publishing unverified reports, or publish immediately with "unverified" badge?
4. **Geographic Granularity**: What level of location precision to display? (Exact coordinates could endanger sources/victims)
5. **Historical Data Depth**: How far back should historical data go? (1 year, 5 years, 10 years?)
6. **API Rate Limits**: What are sustainable rate limits for free tier without incurring excessive API costs?
7. **Content Moderation**: How to handle user-generated content if we add it in future versions?
8. **Ethical Boundaries**: Should we track certain conflict types (e.g., terrorism) differently to avoid stigmatization?
9. **Data Retention**: How long to store detailed event data vs. aggregated statistics? (GDPR compliance)
10. **Monetization Strategy**: Long-term plan for sustainability without compromising neutrality?

## Constraints

### Technical Constraints
- [ ] Must use open-source mapping libraries (MapLibre/Leaflet) to avoid licensing costs
- [ ] PostgreSQL with PostGIS required for geospatial queries
- [ ] Redis caching mandatory for performance requirements
- [ ] Docker containerization required for deployment consistency
- [ ] Ollama Cloud models only for AI/ML (no local GPU dependency)

### Legal Constraints
- [ ] Must comply with GDPR for EU users
- [ ] Must respect API terms of service for all data sources
- [ ] Must implement DMCA takedown process for copyrighted content
- [ ] Must maintain data sovereignty (user data stored in appropriate regions)

### Ethical Constraints
- [ ] Must maintain strict political neutrality (no editorial positions)
- [ ] Must protect source anonymity where applicable
- [ ] Must avoid sensationalism in conflict reporting
- [ ] Must consider safety implications of real-time conflict data (could endanger civilians or aid workers)
- [ ] Must provide context to avoid dehumanizing conflict victims
- [ ] Must be transparent about data limitations and verification status

### Resource Constraints
- [ ] Initial budget: $500/month for API subscriptions (NewsAPI, ACLED premium tier)
- [ ] Team: 4 agents (Tony, Peter, Heimdall, Pepper) + Jarvis coordinator
- [ ] Timeline: MVP launch within 6 weeks from requirements approval
- [ ] Infrastructure: Cloud-hosted (AWS/GCP/Azure) with auto-scaling

## Success Metrics

### User Metrics
- **MAU (Monthly Active Users)**: Target 10,000 MAU within 6 months of launch
- **User Retention**: ≥40% of users return weekly
- **Alert Engagement**: ≥25% of registered users create at least one alert
- **API Adoption**: ≥500 API keys issued within 3 months

### Data Quality Metrics
- **Verification Accuracy**: ≥90% of "verified" events confirmed by manual review
- **Source Diversity**: Average ≥3 sources per verified event
- **False Positive Rate**: ≤5% of flagged misinformation events are actually accurate
- **Data Freshness**: ≥95% of high-severity events updated within 15 minutes

### Performance Metrics
- **Uptime**: ≥99.5% (≤4 hours downtime/month)
- **Page Load Time**: ≤3 seconds for initial map load
- **API Response Time**: ≤500ms for 95th percentile
- **Data Ingestion Latency**: ≤5 minutes from source publication to WarTracker display

### Impact Metrics
- **Media Citations**: ≥50 news articles citing WarTracker data within 6 months
- **Academic Usage**: ≥10 research papers using WarTracker data within 1 year
- **NGO Partnerships**: ≥5 humanitarian organizations using WarTracker operationally
- **Geographic Coverage**: Active conflicts tracked in ≥50 countries

### Operational Metrics
- **Cost per User**: ≤$0.10/month per active user
- **API Cost Efficiency**: ≥80% reduction in external API calls through caching
- **Automation Rate**: ≥90% of data ingestion automated (≤10% manual intervention)
- **Security Incidents**: 0 critical security breaches in first year

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| v0.1 | 2026-03-01 | Pepper | Initial requirements document |

## Review Status

- [ ] Requirements reviewed by Jarvis (Coordinator)
- [ ] Ready for Tony (Architecture phase)
- [ ] Stakeholder approval pending

---

**Next Phase**: Tony (Architect) will create system architecture based on these requirements.
**Document Location**: `docs/agent-workflow/REQ.md`
**GitHub**: https://github.com/humac/WarTracker
