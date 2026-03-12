# WarTracker UI Handoff

## What this handoff is
Implementation-oriented designer notes for Tony and Peter based on the current app, current requirements, and the second-pass design direction.

## What this handoff is not
- not runtime signoff
- not a pixel-perfect Figma file
- not permission to invent a different product

The goal is to give engineering enough structure to implement the next UI pass without guessing at hierarchy, naming, or states.

---

## 1. Deliverables in this pass
- `UI_UX_REVIEW.md` — concise current-state audit
- `UI_DIRECTION.md` — visual language and system direction
- `MOCKUPS.md` — structured mockup specs for key screens
- `HANDOFF.md` — implementation guidance

---

## 2. Product framing to preserve
WarTracker is a neutral, trust-first conflict monitoring product.

When implementing:
- preserve the serious navy/slate foundation
- reduce emoji-heavy presentation
- make credibility cues more prominent than “breaking news” theatrics
- keep language analytical and non-sensational

---

## 3. Information Architecture Changes

## Recommended near-term IA
- `/overview`
- `/map`
- `/timeline`
- `/alerts` internally, but labeled **Priority Feed** until alert-rule management exists
- `/methodology`

### If engineering cannot split routes immediately
Keep one route temporarily, but structure it like route-level screens inside a shared app shell. Do not keep the current “one big card + 3 tabs + stat cards” pattern as the long-term UX.

---

## 4. Priority Implementation Order

### Phase A — Shell and hierarchy
1. Replace current top-of-page KPI emphasis with a compact status strip
2. Establish top app bar / primary navigation with clearer labels
3. Add visible methodology access in header

### Phase B — Shared event primitives
Build reusable components first:
- `EventRow`
- `VerificationBadge`
- `SeverityBadge`
- `ConfidenceBadge` or `ConfidenceLabel`
- `FreshnessLabel`
- `SourceCount`
- `EventDetailPanel`
- `FilterRail`
- `StatusStrip`

### Phase C — Map workspace
Implement the three-zone workspace:
- left filter rail
- center map
- right event rail/detail

### Phase D — Timeline and Priority Feed
Reuse the same event primitives and detail panel.

---

## 5. Component-Level Notes

## A. App shell
**Need:** one serious, stable frame around all screens.

### Include
- brand
- primary nav
- last sync indicator
- pull latest action
- methodology link

### Avoid
- oversized hero treatment
- emoji in main nav labels

## B. Status strip
Replace current stat cards with compact briefing counters.

### Suggested data points
- new in last 24h
- verified
- developing
- unverified
- source/ingestion health

### Important
This should be one horizontal module, not four large cards.

## C. Event row primitive
Create one reusable event row so Map, Timeline, Overview, and Priority Feed do not diverge visually.

### Required fields in row UI
- headline
- region/country
- event type
- verification status
- severity
- source count
- freshness
- optional summary snippet

### Layout rule
Badges should never overpower the headline.

## D. Event detail panel
Stop using modal-style detail as the primary desktop behavior where possible. Prefer persistent side detail.

### Required sections
1. header
2. summary
3. verification & sources
4. location & context
5. related updates
6. actions

## E. Filter rail
Treat filters as first-class workspace tools.

### Minimum controls
- search
- region
- event type
- severity
- verification status
- recency/date range
- reset

---

## 6. Data Contract Guidance for UI
The current frontend event model is too thin for the intended trust-first UX.

### Current minimal fields observed
- `id`
- `title`
- `latitude`
- `longitude`
- `severity`
- `published_date`
- `country_code`

### UI should be prepared for / backend should expose
- `verification_status`
- `confidence_score` or `confidence_band`
- `source_count`
- `summary`
- `event_type`
- `updated_at`
- `region_name`
- `source_list` preview
- `related_conflict_id` or related events grouping

### Important engineering note
The design direction depends heavily on trust metadata being available in the API. If backend fields do not yet exist, Tony/Peter should still build the component slots and fallback states now.

---

## 7. State Requirements
These should be explicitly implemented, not implied.

### Overview
- loading
- no new developments
- active with critical items

### Map workspace
- loading map/list
- no results after filtering
- marker selected
- selected event removed by filters
- stale data / refresh in progress

### Timeline
- empty time range
- normal active list
- selected detail state

### Priority Feed
- no high-priority results
- active feed
- reviewed/acknowledged state placeholder even if persistence comes later

### Event detail
- loading
- no source metadata available
- verified / developing / unverified visual variations

---

## 8. Accessibility Notes
- do not rely on color alone for severity or verification
- preserve keyboard navigation order across nav, filters, list, map, detail
- map interactions must have list/detail equivalents
- timestamps and badges need text labels readable by assistive tech
- avoid icon-only controls without labels/tooltips

---

## 9. Copy / Naming Guidance
Use calmer, more precise labels.

### Preferred labels
- Overview
- Map
- Timeline
- Priority Feed
- Methodology
- Verification
- Confidence
- Sources
- Updated

### Avoid as primary UI language
- flashy marketing phrasing
- excessive emojis
- ambiguous “alerts” wording if the feature is really just a feed

---

## 10. Practical Build Notes for Tony
Tony should translate this into:
- page-level structure
- component breakdown
- spacing tokens / visual rules
- route recommendations
- shared event object assumptions

Tony should not stop at critique; the architecture/task breakdown should map to these screen patterns directly.

---

## 11. Practical Build Notes for Peter
Peter should implement in this order:
1. shell + nav + status strip
2. shared event row + badges + detail panel
3. map workspace layout
4. timeline reuse
5. priority feed reuse

### Implementation caution
Do not overfit to currently missing backend fields. Build the UI with graceful placeholders such as:
- `Verification pending`
- `Source details unavailable`
- `Confidence not yet calculated`

This lets the interface move toward the intended state without blocking on full data parity.

---

## 12. Acceptance Checks for Design Fidelity
Before implementation is considered faithful to this handoff, the build should visibly demonstrate:
- a route- or shell-based IA more structured than current tabs
- a map workspace with filters + map + event rail
- verification/source/freshness visible in primary event surfaces
- a denser timeline than current accordion cards
- a priority feed that is clearly differentiated from true alert-rule management
- a reusable event detail panel across multiple screens

---

## 13. Known Constraint
This handoff is intentionally grounded in the current app. It does not assume full backend support already exists for all trust metadata. Where the data model is incomplete, the UI should still establish layout slots, labels, and fallback copy so the product can evolve without another structural redesign.

---

## 14. Short User-Facing Summary
WarTracker’s next UI pass should feel less like a simple tabbed dashboard and more like a calm, trustworthy analysis workspace. The biggest visible changes are a briefing-style overview, a real map workspace with filters and synchronized detail, a cleaner timeline for change tracking, and stronger verification/source cues throughout the product.
