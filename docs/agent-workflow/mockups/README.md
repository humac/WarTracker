# WarTracker Static Mockups

This folder contains **review-only visual mockups** for WarTracker.

## Purpose
These files are meant to act like lightweight Figma-style review artifacts using static HTML/CSS so the team can evaluate layout, tone, hierarchy, and component direction before implementation work starts.

## Important
- These files are **not production UI**.
- They are intentionally separated from the real frontend.
- They use shared tokens/styles in `styles.css` plus one HTML file per screen.

## Screens
- `overview.html` — briefing / overview screen
- `map-workspace.html` — three-zone map workspace
- `timeline.html` — dense chronological timeline
- `priority-feed.html` — review-first alerts/priority feed direction
- `event-detail.html` — standalone shared detail panel composition
- `index.html` — simple entry page linking to all mockups

## Shared design choices reflected here
- trust-first hierarchy
- navy / slate foundation with restrained crimson/amber accents
- verification shown before severity in most list/detail contexts
- persistent right-rail detail model on desktop
- calm analytical tone rather than sensational news styling
- map views use a more realistic static cartography pass: geopolitical region labels, dashed analyst focus areas, density/heat treatment, corridor overlays, scale treatment, and map-control framing so the product direction reads as conflict intelligence rather than generic dashboard art

## Screenshot outputs
Screenshot PNGs are exported into this same folder with names like:
- `overview.png`
- `map-workspace.png`
- `timeline.png`
- `priority-feed.png`
- `event-detail.png`

## How to review locally
Open any HTML file directly in a browser from this folder, or review the exported PNGs.
