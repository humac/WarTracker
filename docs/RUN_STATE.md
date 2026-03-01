# RUN_STATE.md - WarTracker

**Last Updated:** 2026-03-01T20:15:00Z  
**Current Phase:** pepper_reqs ✅ COMPLETE → Ready for tony_design  
**Owner:** Pepper (Operations Analyst)

---

## Active Pipeline

| Phase | Agent | Session Key | Status | Started | Completed |
|-------|-------|-------------|--------|---------|-----------|
| **jarvis_intake** | Jarvis | — | ✅ COMPLETE | 2026-03-01 19:48 | 2026-03-01 19:55 |
| **pepper_reqs** | Pepper | a6bffbd1-8d72-4daa-aca9-4aa147c97bb2 | ✅ COMPLETE | 2026-03-01 20:04 | 2026-03-01 20:15 |
| **tony_design** | Tony | — | ⏳ READY TO SPAWN | — | — |
| **peter_build** | Peter | — | ⏳ QUEUED | — | — |
| **heimdall_test** | Heimdall | — | ⏳ QUEUED | — | — |
| **pepper_closeout** | Pepper | — | ⏳ QUEUED | — | — |

---

## Current Phase: pepper_reqs

**Status:** ✅ COMPLETE  
**Agent:** Pepper (Operations Analyst)  
**Session:** a6bffbd1-8d72-4daa-aca9-4aa147c97bb2  
**Started:** 2026-03-01 20:04 UTC  
**Completed:** 2026-03-01 20:15 UTC  

## Deliverables
- ✅ docs/agent-workflow/REQ.md - Comprehensive requirements (30 user stories, 40+ functional requirements)
- ✅ docs/agent-workflow/ISSUES.md - Issues log (ambiguities, challenges, ethical concerns, blockers)
- ✅ README.md - Already updated (project overview)

## Requirements Summary

**User Stories:** 30 total
- High Priority (MVP): 10 stories (US-1 to US-10)
- Medium Priority (v1.0): 10 stories (US-11 to US-20)
- Low Priority (Future): 10 stories (US-21 to US-30)

**Functional Requirements:** 40+ total
- Data Collection: 8 requirements
- Data Processing: 8 requirements
- User Interface: 12 requirements
- Alerts & Notifications: 7 requirements
- User Management: 7 requirements
- API & Integration: 5 requirements

**Non-Functional Requirements:** 20+ total
- Performance: 6 requirements
- Security: 8 requirements
- Reliability: 6 requirements
- Scalability: 3 requirements
- Accessibility: 4 requirements
- Maintainability: 4 requirements

**Data Sources Identified:**
- Primary: 5 sources (GDELT, ACLED, NewsAPI, UN OCHA, US State Department)
- Secondary: 10 sources (NGOs, news wires, social media, satellite imagery)

**MVP Acceptance Criteria:** 10 clear, measurable criteria

**Key Issues Documented:**
- 5 ambiguities requiring resolution
- 6 technical challenges identified
- 5 ethical concerns flagged
- Multiple dependencies and blockers documented

---

## Next Phase: tony_design

**Agent:** Tony (Architect)  
**Objective:** Create system architecture based on requirements  
**Model:** ollama/kimi-k2.5:cloud (primary) or ollama/qwen3.5:35b-cloud (backup)  
**Ready to Spawn:** YES  

**Tony's Mission:**
1. Read REQ.md and ISSUES.md
2. Design system architecture (ARCH.md)
3. Create implementation task list (TASKS.md)
4. Address open technical challenges
5. Define database schema
6. Plan verification pipeline
7. Design API structure

---

## Pipeline Status: 🟢 READY FOR TONY

---

## Autonomy Enforcement

**Pre-Flight Check Required Before Every Reply:**
1. ☐ Check `subagents list` for completed runs
2. ☐ Reconcile with this file (phase/status mismatch?)
3. ☐ If completed → spawn next phase within 30s
4. ☐ If failed → retry/fallback within 30s
5. ☐ Then reply to user

**Handoff SLA:** 120 seconds max from phase completion → next spawn

---

## Notes for Tony

**Key Architecture Decisions Needed:**
1. Database schema for conflict events (flexible for unknown sources)
2. Multi-source verification algorithm
3. Geospatial indexing strategy (PostGIS)
4. Real-time data pipeline (async collectors + Redis queue)
5. API design (RESTful, versioned)
6. Caching strategy (multi-layer)
7. Frontend component architecture

**Open Questions from REQ.md:**
- Data licensing (legal review needed)
- Casualty count discrepancy handling
- Geographic precision vs. safety
- Real-time vs. verification tradeoff
- Historical data depth

**Ethical Concerns to Address:**
- Neutrality & bias mitigation
- Harm to vulnerable populations (coordinate blurring)
- Misuse prevention
- Privacy protection

**See ISSUES.md for full details.**
