# WarTracker Mockup Specs

## Purpose
These are structured pre-build mockup specifications for implementation and review. They are not abstract ideas; they describe the intended screen composition, hierarchy, spacing, and behavior closely enough for Tony and Peter to build from.

All mockups are grounded in the current product and required feature set.

---

# 1. Overview / Briefing Screen

## User goal
Understand what changed, where it changed, and how trustworthy the latest reporting is in under 30 seconds.

## Desktop layout

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ Top App Bar: WarTracker | Overview | Map | Timeline | Priority Feed | Method │
│                            Last sync 12:31 UTC | Pull latest | User/Theme    │
├──────────────────────────────────────────────────────────────────────────────┤
│ Status Strip                                                               │
│ [New 24h: 18] [Verified: 11] [Developing: 5] [Unverified: 2] [Sources OK] │
├──────────────────────────────────────────────────────────────────────────────┤
│ Critical Developments                                                      │
│ ┌────────────────────────────┬────────────────────────────┬───────────────┐ │
│ │ Event A                    │ Event B                    │ Event C       │ │
│ │ badges + time + summary    │ badges + time + summary    │ ...           │ │
│ └────────────────────────────┴────────────────────────────┴───────────────┘ │
├──────────────────────────────────────────────────────────────────────────────┤
│ Main Split                                                                   │
│ ┌──────────────────────────────────────┬───────────────────────────────────┐ │
│ │ Map Preview                          │ Live Priority Feed                │ │
│ │ compact world map                    │ ranked rows                       │ │
│ │ hotspot clusters                     │ headline                          │ │
│ │ legend                               │ metadata                          │ │
│ │ CTA: Open full map workspace         │ CTA: View all                     │ │
│ └──────────────────────────────────────┴───────────────────────────────────┘ │
├──────────────────────────────────────────────────────────────────────────────┤
│ Trend Row: [Hotspot Regions] [Escalating Conflicts] [Source Coverage]       │
└──────────────────────────────────────────────────────────────────────────────┘
```

## Spacing / rhythm
- page padding: 24px desktop
- gap between major modules: 24–32px
- status strip internal padding: 12–16px
- critical cards internal padding: 16px

## Module specs

### A. Top app bar
**Left:** brand + primary nav  
**Right:** last sync time, pull latest button, methodology access, optional theme/user actions

**Behavior:**
- Overview nav item visibly active
- methodology link always visible, not buried in footer

### B. Status strip
**Purpose:** operational health and briefing at a glance

**Content order:**
1. new events last 24h
2. verified count
3. developing count
4. unverified count
5. source health / ingestion status

**Visual treatment:**
- one horizontal panel
- subdued background
- compact tokens, not giant cards

### C. Critical Developments
**Format:** 3 to 5 horizontally aligned cards or stacked compact cards depending on width

**Each card contains:**
- headline, max 2 lines
- verification badge first
- severity badge second
- updated time
- 1-line summary snippet
- region label

**States:**
- if no critical items, module title becomes “Key Developments” and shows highest-change items instead

### D. Map preview
**Map content:**
- simplified preview of current global hotspots
- clustered markers
- legend in lower-left
- selected preview optional but not required

**Action:**
- `Open full map workspace`

### E. Live Priority Feed preview
Show 5–7 rows.

**Each row:**
- headline
- region
- verification badge
- severity badge
- source count
- freshness

## Key states

### Empty
- message: `No new developments in the selected briefing window.`
- action: `Expand to last 7 days`

### Loading
- skeleton strip + skeleton cards + muted map block

### Active
- normal state with one clearly dominant critical item if one exists

---

# 2. Map Workspace

## User goal
Explore conflict activity geographically, filter the result set, and inspect a selected event without losing context.

## Desktop layout

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ Top App Bar                                                                 │
├───────────────┬──────────────────────────────────────┬───────────────────────┤
│ Filter Rail   │ Map Surface                          │ Event Rail            │
│ 280–320px     │ Flexible                             │ 360–420px             │
│               │                                      │                       │
│ Search        │ ┌──────────────────────────────────┐ │ Results header        │
│ Region        │ │                                  │ │ 42 events             │
│ Event type    │ │           world / region map     │ │ active filter chips   │
│ Severity      │ │           markers + clusters      │ │                       │
│ Verification  │ │                                  │ │ [list state]          │
│ Date range    │ │ legend       map controls        │ │ event rows            │
│ Reset         │ └──────────────────────────────────┘ │                       │
│               │                                      │ [selected detail]      │
└───────────────┴──────────────────────────────────────┴───────────────────────┘
```

## Zone specs

### A. Filter rail
**Sections in order:**
1. search input (`Search country, region, actor, event`)
2. region selector
3. event type multi-select
4. severity chips / checkbox group
5. verification chips
6. recency or date range
7. reset all filters

**Interaction notes:**
- active filters appear both in the rail and as removable chips above results
- rail stays sticky while center/right panes scroll

### B. Map surface
**Always visible items:**
- map itself
- severity legend
- map controls (zoom, fit results)
- result count feedback in top-left or top overlay

**Marker behavior:**
- clusters at wide zoom
- single markers with severity encoding
- selected marker gets ring/halo
- hover on list row temporarily emphasizes marker

### C. Event rail
Two states:

#### Default state: event list
**Header:**
- result count
- sort dropdown (`Priority`, `Newest`, `Most sources`)
- active filter chips

**Row structure:**
- headline
- summary snippet, max 2 lines
- metadata row: `Region · Type · 3 sources · Updated 12m ago`
- badge row: verification then severity

#### Selected state: detail panel within rail
Detail panel can replace top of list or pin above it.

**Sections:**
1. event header
2. summary
3. context/location
4. verification & sources
5. related updates
6. actions

## Selected detail wireframe

```text
┌─────────────────────────────────────┐
│ [Verified] [Critical]   Updated 12m │
│ Headline                              │
│ Region / Country · Event type         │
│--------------------------------------│
│ Summary                               │
│ Neutral 2–3 sentence synopsis         │
│--------------------------------------│
│ Verification & Sources                │
│ High confidence                       │
│ 3 sources                             │
│ Reuters · GDELT · ReliefWeb           │
│--------------------------------------│
│ Location & Context                    │
│ Approx. area / actors / conflict id   │
│--------------------------------------│
│ Recent Related Updates                │
│ - 10:20 UTC ...                       │
│ - 08:10 UTC ...                       │
│--------------------------------------│
│ [Open source links] [Copy link]       │
└─────────────────────────────────────┘
```

## States

### Empty results
- keep map visible
- right rail says: `No events match current filters.`
- provide `Reset filters`

### Loading
- map shell visible immediately
- list shows 8 skeleton rows
- detail panel skeleton if selection is preserved

### Selection during refresh
- preserve selected event if still in result set
- if removed by filters, show message: `Selected event hidden by current filters`

---

# 3. Timeline View

## User goal
Scan changes over time, identify escalation, and open shared event detail quickly.

## Desktop layout

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ Top App Bar                                                                 │
├──────────────────────────────────────────────────────────────────────────────┤
│ Sticky Timeline Filter Bar                                                  │
│ Search | Region | Type | Severity | Verification | Date range | Sort        │
├───────────────────────────────────────────────┬──────────────────────────────┤
│ Timeline List                                 │ Shared Detail Panel          │
│                                               │                              │
│ 12 Mar 2026                                   │ selected event details       │
│  12:31  [Verified][High] Headline             │ same component model as map  │
│        Region · sources · updated             │                              │
│  10:20  [Developing][Elevated] Headline       │                              │
│                                               │                              │
│ 11 Mar 2026                                   │                              │
│  22:08  [Unverified][Moderate] Headline       │                              │
└───────────────────────────────────────────────┴──────────────────────────────┘
```

## Design direction
The timeline should be denser than the current accordion. Day separators remain, but event rows should feel like a professional log, not stacked marketing cards.

## Row spec
Each timeline row includes:
- timestamp on left
- headline
- optional one-line summary
- metadata row: region, event type, source count
- badges: verification first, severity second
- state chips when applicable: `New`, `Escalated`, `Updated`, `Verified`

## Spacing
- day separator padding top: 24px
- row vertical padding: 12px
- row gap: 8px
- timestamp column width: 72–88px

## Interaction notes
- clicking row opens detail panel on right
- keyboard arrows can step through rows in dense mode
- filters remain sticky when scrolling long histories

## States

### Empty
`No timeline events for this time range.`

### Loading
Skeleton day separators + row placeholders.

### Active detail
Selected row receives subtle background emphasis and left rule.

---

# 4. Alerts / Priority Feed

## User goal
Rapidly review the most important current items without pretending this is already a full alert-rule system.

## Naming note
Until alert rule creation exists, this screen should be presented as **Priority Feed**.

## Desktop layout

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ Top App Bar                                                                 │
├──────────────────────────────────────────────────────────────────────────────┤
│ Feed Controls                                                               │
│ Severity | Verification | Region | Sort | Show acknowledged                 │
├───────────────────────────────────────────────┬──────────────────────────────┤
│ Priority Feed List                            │ Detail / Review Panel        │
│                                               │                              │
│ [Critical] [Verified] Headline                │ selected event detail        │
│ Region · 4 sources · 8m ago                   │ acknowledgement state        │
│ Short synopsis                                │ source block                 │
│                                               │ actions                      │
│ [High] [Developing] Headline                  │                              │
│ ...                                           │                              │
└───────────────────────────────────────────────┴──────────────────────────────┘
```

## Feed row spec
- severity badge first only if user sorts primarily by severity; otherwise verification can lead
- headline max 2 lines
- 1-line synopsis
- metadata row with source count and updated time
- optional review state chip: `Unreviewed`, `Reviewed`, `Acknowledged`

## Above-feed summary strip
Instead of three colorful numeric cards, use compact counters:
- Critical now
- Escalated in last 24h
- Awaiting review

## States

### No high-priority items
Message: `No current items meet the selected priority threshold.`

### Loading
Skeleton list rows; keep summary strip visible.

### Empty because all acknowledged
Message: `All current priority items have been reviewed.`

---

# 5. Event Detail Panel / Drawer

## Purpose
One shared detail pattern used from Map, Timeline, Overview, and Priority Feed.

## Desktop pattern
Right-side panel, 360–420px wide.

## Mobile pattern
Bottom sheet at 75–90% screen height.

## Structure

```text
Header
- verification badge
- severity badge
- freshness/time
- headline
- region / event type / conflict grouping

Section 1: Summary
- 2–3 sentence neutral synopsis

Section 2: Verification & Sources
- confidence label
- source count
- source list with source names + timestamps
- methodology note / link

Section 3: Location & Context
- country / region
- approximate location if blurred
- actor/context fields if available

Section 4: Related Developments
- short reverse-chronological linked updates

Section 5: Actions
- open source links
- copy link
- export JSON/CSV when available
- save/bookmark later when implemented
```

## Visual rules
- trust block gets its own section, not buried
- action area stays at bottom with clear separation
- avoid modal-on-modal behavior on desktop

## Key states

### Loading
Preserve shell and section headings; use line skeletons.

### Missing source detail
Show explicit note: `Detailed source metadata not yet available for this event.`

### Unverified
Use caution styling but keep calm tone. Avoid alarming banners unless risk is confirmed.

---

# Cross-Screen Shared Rules

## Event metadata order
Use the same metadata order everywhere:
`Region · Event type · Verification · Confidence · Sources · Updated`

## Badge order
1. Verification
2. Severity
3. State chips (`New`, `Escalated`, `Acknowledged`)

## Timestamp format
- collapsed: relative time (`12m ago`)
- expanded: exact UTC (`12 Mar 2026 12:31 UTC`)

## Empty-state voice
Clear, factual, non-cute.

## Short User-Facing Summary
The redesigned WarTracker shifts from a simple tabbed dashboard to a proper intelligence workspace. The new direction adds a briefing-style overview, a real map workspace with filters and synced details, a denser timeline for trend reading, and a more honest priority feed. Across all screens, verification, confidence, source count, and freshness become visible parts of the interface rather than hidden details.
