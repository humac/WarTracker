# WarTracker UI Direction

## Intent
Define a visual and interaction direction that matches WarTracker’s actual mission: calm, trustworthy, neutral situational awareness for repeated daily use.

This direction is grounded in:
- current WarTracker implementation
- `REQ.md` mission and user stories
- `ARCH.md` feature intent
- existing navy/slate/crimson design system work

---

## 1. Product Tone
WarTracker should feel:
- **Calm** — never sensational
- **Credible** — evidence and status always visible
- **Operational** — built for repeated scanning and triage
- **Neutral** — analytical, not dramatic
- **Dense but controlled** — information-rich without becoming noisy

### Anti-goals
Avoid making the UI feel:
- like a newsroom breaking-news banner
- like a consumer social feed
- like a generic SaaS KPI dashboard
- like a military game interface

---

## 2. Visual Language

### Base palette
Keep the existing foundation, but tighten usage.

- **Background:** deep navy / graphite surfaces
- **Primary text:** off-white / cool gray
- **Secondary text:** muted slate
- **Borders:** low-contrast cool gray lines
- **Critical accent:** crimson only for true urgency
- **Warning accent:** amber for developing/elevated states
- **Stable/verified accent:** desaturated teal or blue-gray, not celebratory green

### Color role guidance
- **Severity** communicates impact
- **Verification** communicates trust
- **Freshness** communicates recency

These should not collapse into one color system.

#### Recommended semantic mapping
- Severity 1–2: muted olive / desaturated green-gray
- Severity 3: amber
- Severity 4: red-orange
- Severity 5: crimson
- Verified: blue-gray / teal badge
- Developing: amber outline badge
- Unverified: slate/outline with caution icon
- Stale data: neutral muted treatment

### Contrast intent
Use dark surfaces with enough contrast for long reading sessions. Avoid fully black backgrounds and neon accents.

---

## 3. Typography & Hierarchy

### Typographic character
Editorial, compact, and factual. Headings should establish structure; metadata should do most of the work.

### Hierarchy levels
1. **Screen title / briefing title**
2. **Module title**
3. **Event headline**
4. **Metadata line**
5. **Supporting note / disclaimer / methodology**

### Rules
- Headlines should be sentence case, not overly branded
- Metadata rows should be consistent across all views
- Timestamps should be explicit and use **UTC**
- Avoid excessive bolding; rely on spacing and alignment

---

## 4. Layout System

### Global shell
Use a desktop-first shell with:
- top app bar
- left primary navigation rail or compact top nav
- main content region
- optional persistent right-side contextual panel on workspace screens

### Desktop max-width behavior
- Overview: centered but wide, ~1440px comfortable maximum
- Workspace screens: full-bleed inside app shell with controlled interior gutters

### Spacing rhythm
Use an 8px spacing base.

#### Recommended practical tokens
- 4px: hairline adjacency only
- 8px: micro spacing inside metadata groups
- 12px: chip/badge to text separation
- 16px: standard card/panel padding on dense rows
- 24px: section spacing inside modules
- 32px: major module separation

### Surface model
Reduce over-nesting.
- Prefer one clear panel boundary per functional area
- Avoid card-inside-card-inside-card unless state separation requires it
- Let background tone differences define structure where possible

---

## 5. Information Hierarchy by Screen Type

### Overview
The screen should answer:
1. what changed
2. where it changed
3. how serious it is
4. how trustworthy the reporting is

### Map workspace
The screen should support:
1. filter
2. scan geography
3. inspect a candidate event
4. compare event list with map state
5. judge trust quickly

### Timeline
The screen should optimize:
1. chronological scanning
2. escalation recognition
3. opening shared event details

### Priority Feed
The screen should optimize:
1. high-priority triage
2. acknowledgement / review state
3. rapid open-detail workflow

---

## 6. Trust Signals (Mandatory)
WarTracker’s credibility depends on these being visible without opening a deep detail page.

### Required trust metadata on every important event row/card
- verification status
- confidence band or score
- source count
- timestamp
- freshness label
- region/country

### Trust signal behavior
- **Verification badge** should appear before severity badge in list/detail contexts
- **Confidence** should be shown as a compact label: High / Medium / Low confidence
- **Source count** should be plain language: `3 sources`, `1 source`, etc.
- **Freshness** should use relative plus exact time when expanded: `Updated 12m ago · 12 Mar 2026 12:31 UTC`
- **Methodology link** should be visible in header and detail views

### Trust panel pattern
On detail surfaces, add a dedicated “Verification & Sources” block rather than hiding trust data in generic metadata.

---

## 7. Core Component Patterns

### A. Top status strip
Purpose: fast briefing, not vanity metrics.

Contains:
- last ingestion time
- new events in last 24h
- verified / developing / unverified counts
- source health or ingestion status

Pattern notes:
- compact horizontal strip
- uses subdued panel styling
- not a hero banner

### B. Critical developments module
Purpose: show 3–5 highest priority items.

Each row includes:
- headline
- country/region
- verification badge
- severity badge
- updated time
- 1-line summary

### C. Filter rail
For Map and Timeline.

Sections:
- search
- region
- event type
- severity
- verification status
- date range / recency
- reset all

Rules:
- filters persist while user navigates between related views where possible
- section labels remain visible during scroll
- active filters shown as removable chips near top of workspace

### D. Event list row
Reusable across Overview, Map, Timeline, and Priority Feed.

Structure:
1. left: severity marker / type icon
2. center: headline + summary snippet
3. below: metadata row
4. right: badges, time, disclosure affordance

Metadata row order:
`Region · Event type · Verification · Confidence · Sources · Updated`

### E. Event detail drawer / side panel
Single reusable detail model.

Sections:
1. header
2. summary
3. location/context
4. verification & sources
5. related recent updates
6. actions (open source, copy link, export, save later)

### F. Legend system
The map should always expose a visible, compact legend for:
- severity colors
- verification states
- marker clustering meaning if used

---

## 8. Screen Structure Direction

## Overview / Briefing screen
Recommended vertical sequence:
1. page header + methodology access
2. status strip
3. critical developments
4. map preview + live feed split
5. trend modules / hotspots

## Map workspace
Recommended desktop structure:
- **Left rail:** 280–320px filters
- **Center map:** flexible primary surface
- **Right rail:** 360–420px event list / selected detail

Behavior:
- no modal for primary event inspection on desktop
- selection should persist in right rail
- list and map must stay synchronized

## Timeline
Recommended structure:
- sticky top filter/subnav row
- main two-column chronology or single dense list with day separators
- optional side panel reuse for selected event

## Priority Feed
Recommended structure:
- compact filter/sort row
- feed list with review state
- detail drawer reuse
- explicit empty state when no priority items match current filter

---

## 9. State Behavior

### Empty states
Empty states should be analytical, not cute.

Include:
- what filter combination caused the result
- one suggested recovery action
- optional reset filters CTA

### Loading states
- use skeleton rows/panels, not spinner-only blocks
- preserve shell and layout while content loads
- for map, load list and contextual info independently where possible

### Error states
- state what failed: map tiles, ingestion status, event fetch, sources
- provide retry action
- keep existing context visible if stale data exists

### Live-update states
When data refreshes:
- show subtle timestamp update
- avoid reflowing selected detail unexpectedly
- flag newly added events with a temporary `New` chip

---

## 10. Responsive Behavior

### Tablet
- collapse three-column map workspace to stacked filter drawer + map + bottom sheet detail

### Mobile
- default to feed-first or summary-first approach
- map launches as full-screen task, not as a cramped embed
- selected event opens bottom sheet, not side panel
- sticky filter bar with count of active filters

Important: mobile may be a later refinement, but desktop layout decisions should not block it.

---

## 11. Interaction Notes
- clicking a marker selects event and highlights corresponding list row
- clicking a row centers map and opens detail
- hovering a row can preview marker emphasis on desktop
- keyboard focus order must move logically: nav → filters → list/map → detail
- route changes should preserve meaningful context where safe

---

## 12. Naming Direction
To better match actual behavior:
- `Alerts` → **Priority Feed** until rule-based alerts are built
- `Dashboard` → **Overview** or **Briefing**
- `Map` stays **Map**
- `Timeline` can be labeled **Timeline** or **Recent Developments**
- add **Methodology** as a visible trust route

---

## 13. Short User-Facing Summary
WarTracker is moving from a simple dashboard into a clearer intelligence workspace. The redesign keeps the serious navy/crimson foundation, but shifts focus toward trust, clarity, and investigation. Users will see stronger verification cues, a real map workspace with filters and synchronized detail, a denser timeline, and a more honest priority feed instead of a generic tabbed dashboard.
