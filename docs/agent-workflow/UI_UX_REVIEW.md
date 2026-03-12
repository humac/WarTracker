# WarTracker UI/UX Review

## Scope
Second-pass design audit of the current WarTracker frontend as implemented in `frontend/app/page.tsx` and supporting components (`ConflictMap`, `Timeline`, `Alerts`), cross-checked against `REQ.md`, `ARCH.md`, and prior redesign notes.

## Current Product Reality
WarTracker currently ships as a single-page dashboard with:
- sticky top header
- three in-page tabs: Map, Timeline, Alerts
- four summary cards
- one large content card that swaps tab content
- footer with legal links

### Current component behavior
- **Map**: Leaflet map with simple colored dot markers and popup metadata (`title`, `severity`, `date`, `country_code`)
- **Timeline**: expandable by-date groups with severity-tinted cards
- **Alerts**: severity-filtered event feed with modal details, but not true alert-rule management

## What Works
1. **Serious baseline tone**  
   The navy/slate/crimson palette is directionally correct for a geopolitical tracking product.
2. **Clear top-level concepts**  
   Map, Timeline, and Alerts are the right major views for this domain.
3. **Reasonable first-pass component system**  
   shadcn/ui gives a stable implementation base for a more mature design system.
4. **Readable severity language**  
   Low / Moderate / Elevated / High / Critical is more usable than raw numeric scales.
5. **Basic loading and error states exist**  
   The app at least acknowledges loading/failure conditions.

## Main UX Gaps

### 1. Information architecture is flatter than the product promise
The product is positioned as a trustworthy situational-awareness platform, but the UI behaves like a compact demo dashboard.

**Observed:**
- one route, one card shell, three local tabs
- no distinct overview/briefing layer
- no dedicated map workspace
- no methodology/trust surface in the primary workflow

**Impact:**
Users cannot quickly answer:
- What changed today?
- What is highest priority?
- Which reports are trustworthy?
- Where should I focus next?

### 2. Map is visual, not operational
The map is the centerpiece, but it lacks the surrounding tools analysts need.

**Missing around the map:**
- search
- persistent filters
- synchronized event list
- selected-event drawer/panel
- trust metadata adjacent to selection
- fit-to-results / selection persistence behavior

**Result:**
Users can see markers, but cannot effectively triage or investigate.

### 3. Trust signals are not first-class
Requirements emphasize verification, confidence, source visibility, and neutrality. The implemented UI mostly exposes severity and recency.

**Current trust gaps:**
- no verification badge visible in main views
- no confidence band or confidence score treatment
- no source count in cards, list rows, or popups
- no freshness/data latency treatment beyond generic “Last Update”
- no methodology/neutrality reinforcement near decision surfaces

**Design implication:**
WarTracker should visually prioritize credibility before urgency.

### 4. Too much emphasis on generic dashboard cards
The four KPI cards consume prime space, but the app’s actual value is analytical workflow, not vanity metrics.

**Problem:**
- the user must scan generic metrics before reaching live analysis
- the central work area feels boxed into a single oversized card
- the UI reads more like admin analytics than briefing + investigation tooling

### 5. Alerts labeling is misleading
The current Alerts view is a severity feed, not an alert-management system.

**Missing from actual alert UX:**
- saved rules
- threshold logic
- geography targeting
- channel delivery
- pause/active states
- trigger history / acknowledgement

**Recommendation:**
Short-term rename to **Priority Feed** in the product language unless rule-based alerts are actually built.

### 6. Timeline is readable but too bulky for repeated use
The accordion-by-date pattern works for light browsing, but not for dense analytical scanning.

**Current issues:**
- large vertical footprint
- repeated card shells
- weak comparative scanning across dates
- no new / escalated / verified cues

### 7. Current iconography and tone are slightly too consumer-like
Emoji-driven navigation and stat cards reduce perceived credibility for a serious conflict-tracking interface.

**Recommendation:**
Use restrained iconography, text labels, and metadata lines instead of emoji-heavy labeling.

## Requirements / UI Mismatch
The written requirements and architecture call for:
- verification badges
- source lists
- filters by region/type/date
- event detail panels
- search
- export workflows
- customizable alerts
- neutrality disclaimers throughout

The current implementation delivers only a thin slice of that product story. This is the most important design issue: **expectation and interface are currently misaligned.**

## Design Priorities
1. **Make Map the primary operational workspace**
2. **Expose trust metadata in every key event surface**
3. **Separate briefing, exploration, and feed consumption into clearer screens**
4. **Create one reusable event-detail model across map/timeline/feed**
5. **Replace decorative dashboard chrome with analytical hierarchy**

## Immediate Recommendations

### Near-term, high-value
- Introduce route-level IA: Overview, Map, Timeline, Priority Feed, Methodology
- Rebuild Map as a three-zone workspace: filter rail / map / event rail
- Add verification, confidence, source count, freshness to event rows and detail panel
- Replace top stat emphasis with a compact status strip + critical developments module
- Reframe current Alerts as Priority Feed until true rules exist

### Later, when backend/UI model supports it
- true alert-rule management
- saved views and bookmarks
- comparative analytics
- methodology/source health dashboard
- mobile-specific condensed workflows

## Summary Verdict
WarTracker already has the right subject matter, the right high-level views, and a usable visual foundation. What it lacks is a design system for **trustworthy analysis**. The next design pass should not be more decorative; it should be more operational, more explicit, and more evidence-first.
