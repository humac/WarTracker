# Task List: Map Component Implementation

**Project:** WarTracker  
**Document ID:** TASKS-MAP-001  
**Date:** 2026-03-02  
**Author:** Tony (Architect)  
**Assigned To:** Peter (Developer)  
**Priority:** High  
**Estimated Effort:** 8-12 hours  

---

## Overview

Implement the Leaflet-based map component per `docs/ARCH_MAP_COMPONENT.md`. This task includes marker clustering, accessibility, error handling, and comprehensive testing.

---

## Task Checklist

### Phase 1: Core Implementation (2-3 hours)

- [ ] **TASK-1.1: Update Dependencies**
  - [ ] Install `leaflet.markercluster` and types
  - [ ] Remove MapLibre GL dependencies (if not used elsewhere)
  - [ ] Verify package.json has correct versions:
    ```json
    {
      "leaflet": "^1.9.4",
      "@types/leaflet": "^1.9.21",
      "leaflet.markercluster": "^1.5.3",
      "@types/leaflet.markercluster": "^1.5.4"
    }
    ```

- [ ] **TASK-1.2: Refactor ConflictMap Component**
  - [ ] Import Leaflet and markercluster plugin
  - [ ] Initialize map with OSM tile layer
  - [ ] Implement marker clustering group
  - [ ] Add severity-based marker colors (red/orange/green)
  - [ ] Create custom divIcon markers (lighter than images)
  - [ ] Add popup with event details (title, severity, date, sources)
  - [ ] Implement fitBounds to show all markers on load
  - [ ] Add cleanup on component unmount (`map.remove()`)

- [ ] **TASK-1.3: Add TypeScript Types**
  - [ ] Create `ConflictMap.types.ts` with interfaces:
    ```typescript
    interface ConflictEvent {
      id: number
      title: string
      latitude: number
      longitude: number
      severity: number
      published_date: string
      source_count?: number
      verification_status?: 'verified' | 'developing' | 'unverified'
    }
    
    interface ConflictMapProps {
      events: ConflictEvent[]
      className?: string
      onEventSelect?: (event: ConflictEvent) => void
    }
    
    interface FilterOptions {
      severityMin?: number
      severityMax?: number
      eventTypes?: string[]
      dateFrom?: string
      dateTo?: string
    }
    ```

---

### Phase 2: Marker Clustering (2-3 hours)

- [ ] **TASK-2.1: Implement Clustering**
  - [ ] Import markercluster CSS files
  - [ ] Create marker cluster group with config:
    ```typescript
    const clusterGroup = L.markerClusterGroup({
      maxClusterRadius: 50,
      disableClusteringAtZoom: 10,
      spiderfyOnMaxZoom: true,
      showCoverageOnHover: true,
      zoomToBoundsOnClick: true,
    })
    ```
  - [ ] Add all markers to cluster group (not directly to map)
  - [ ] Add cluster group to map

- [ ] **TASK-2.2: Custom Cluster Icons**
  - [ ] Create custom cluster icon based on severity mix
  - [ ] Use `iconCreateFunction` to customize cluster appearance:
    ```typescript
    iconCreateFunction: (cluster) => {
      const childMarkers = cluster.getAllChildMarkers()
      const maxSeverity = Math.max(...childMarkers.map(m => m.event.severity))
      // Return L.divIcon with color based on maxSeverity
    }
    ```

- [ ] **TASK-2.3: Performance Optimization**
  - [ ] Test with 1,000 markers (measure render time)
  - [ ] Test with 10,000 markers (measure render time)
  - [ ] Optimize if render time >500ms
  - [ ] Implement lazy loading for large datasets (optional)

---

### Phase 3: Loading States & Error Handling (1-2 hours)

- [ ] **TASK-3.1: Loading State**
  - [ ] Add `isLoading` state
  - [ ] Create `<MapSkeleton />` component (animated placeholder)
  - [ ] Show skeleton while map initializes
  - [ ] Hide skeleton when map is ready

- [ ] **TASK-3.2: Error Handling**
  - [ ] Add try-catch around map initialization
  - [ ] Create error state with user-friendly message
  - [ ] Implement fallback UI (event list view) when map fails
  - [ ] Log errors to console with full stack trace
  - [ ] Add retry button for transient errors

- [ ] **TASK-3.3: Empty State**
  - [ ] Handle case when no events match filters
  - [ ] Show friendly message: "No conflicts match your filters"
  - [ ] Provide "Clear Filters" button

- [ ] **TASK-3.4: Invalid Coordinates**
  - [ ] Filter out events with (0, 0) coordinates
  - [ ] Show count: "Showing X of Y events (Z have invalid coordinates)"
  - [ ] Log invalid coordinates to console for debugging

---

### Phase 4: Accessibility (2-3 hours)

- [ ] **TASK-4.1: Keyboard Navigation**
  - [ ] Make markers focusable (`tabIndex="0"`)
  - [ ] Add keydown handler (Enter/Space to open popup)
  - [ ] Implement arrow key panning (optional, advanced)
  - [ ] Add +/- keys for zoom (optional, advanced)

- [ ] **TASK-4.2: Screen Reader Support**
  - [ ] Add ARIA labels to all markers:
    ```typescript
    aria-label={`Conflict event: ${event.title}, Severity ${event.severity} out of 5`}
    ```
  - [ ] Add `role="button"` to markers
  - [ ] Add live region for map updates (announces when markers change)
  - [ ] Ensure popup content is accessible (proper heading hierarchy)

- [ ] **TASK-4.3: Color Independence**
  - [ ] Add icons to markers (not just colors)
  - [ ] Add text labels: "High Severity", "Medium Severity", "Low Severity"
  - [ ] Ensure high contrast (border + fill colors)
  - [ ] Test with colorblind simulator (optional)

- [ ] **TASK-4.4: Focus Management**
  - [ ] Add visible focus indicators on markers
  - [ ] Trap focus inside popup when open
  - [ ] Return focus to marker when popup closes
  - [ ] Test with keyboard-only navigation

- [ ] **TASK-4.5: WCAG Compliance Testing**
  - [ ] Run axe-core or Lighthouse accessibility audit
  - [ ] Fix all critical/high severity issues
  - [ ] Target: WCAG 2.1 AA compliance

---

### Phase 5: Unit Tests (2-3 hours)

- [ ] **TASK-5.1: Setup Test Environment**
  - [ ] Install `@testing-library/react`, `@testing-library/jest-dom`
  - [ ] Install `leaflet` mock or use `jest-canvas-mock`
  - [ ] Configure Jest for Leaflet (mock L.map, L.marker, etc.)

- [ ] **TASK-5.2: Component Tests**
  - [ ] Test: Renders map container
  - [ ] Test: Creates markers for valid events
  - [ ] Test: Filters out invalid coordinates (0, 0)
  - [ ] Test: Shows loading skeleton initially
  - [ ] Test: Shows error UI when initialization fails
  - [ ] Test: Shows empty state when no events

- [ ] **TASK-5.3: Marker Tests**
  - [ ] Test: Markers have correct colors based on severity
  - [ ] Test: Clicking marker opens popup
  - [ ] Test: Popup contains event title, severity, date
  - [ ] Test: Keyboard navigation opens popup (Enter/Space)

- [ ] **TASK-5.4: Clustering Tests**
  - [ ] Test: Markers are clustered at low zoom
  - [ ] Test: Clusters split at high zoom (≥10)
  - [ ] Test: Clicking cluster zooms to bounds
  - [ ] Test: Cluster count is correct

- [ ] **TASK-5.5: Integration Tests**
  - [ ] Test: Component receives events from API and displays them
  - [ ] Test: Filtering events updates markers
  - [ ] Test: Selecting event triggers `onEventSelect` callback

- [ ] **TASK-5.6: Test Coverage**
  - [ ] Run coverage report
  - [ ] Target: ≥80% line coverage
  - [ ] Target: ≥90% branch coverage

---

### Phase 6: Browser Testing (1-2 hours)

- [ ] **TASK-6.1: Desktop Browsers**
  - [ ] Chrome (latest) - Verify map renders, markers display, clustering works
  - [ ] Firefox (latest) - Verify map renders, markers display, clustering works
  - [ ] Safari (latest) - Verify map renders, markers display, clustering works
  - [ ] Edge (latest) - Verify map renders, markers display, clustering works

- [ ] **TASK-6.2: Mobile Browsers**
  - [ ] Mobile Safari (iOS 14+) - Verify touch gestures, marker interaction
  - [ ] Chrome Mobile (Android 10+) - Verify touch gestures, marker interaction

- [ ] **TASK-6.3: Accessibility Testing**
  - [ ] Test with VoiceOver (Mac) or NVDA (Windows)
  - [ ] Test keyboard-only navigation
  - [ ] Verify screen reader announces markers correctly

- [ ] **TASK-6.4: Performance Testing**
  - [ ] Measure initial load time (target: <3 seconds)
  - [ ] Measure marker render time for 1,000 events (target: <500ms)
  - [ ] Measure marker render time for 10,000 events (target: <2 seconds)
  - [ ] Check memory usage (target: <100MB with 10,000 markers)

- [ ] **TASK-6.5: Capture Proof**
  - [ ] Screenshot: Desktop browser with markers visible
  - [ ] Screenshot: Mobile browser with markers visible
  - [ ] Screenshot: Clustered view (zoomed out)
  - [ ] Screenshot: Unclustered view (zoomed in)
  - [ ] Screenshot: Popup with event details
  - [ ] Save screenshots to `docs/screenshots/`

---

### Phase 7: Documentation (1 hour)

- [ ] **TASK-7.1: Code Documentation**
  - [ ] Add JSDoc comments to all functions
  - [ ] Add inline comments for complex logic
  - [ ] Ensure TypeScript types are complete

- [ ] **TASK-7.2: Update README**
  - [ ] Document map component usage
  - [ ] List supported features
  - [ ] Mention accessibility features

- [ ] **TASK-7.3: Tile Provider Documentation**
  - [ ] Document current tile provider (OSM)
  - [ ] Document how to switch to MapTiler (if needed)
  - [ ] Note any API key requirements

- [ ] **TASK-7.4: Update ARCH_MAP_COMPONENT.md**
  - [ ] Mark completed tasks
  - [ ] Note any deviations from architecture
  - [ ] Add performance metrics from testing

---

## Acceptance Criteria

**Definition of Done:**

- [ ] All tasks above completed and checked off
- [ ] Unit tests passing (≥80% coverage)
- [ ] Browser testing completed (all target browsers)
- [ ] Accessibility audit passed (WCAG 2.1 AA)
- [ ] Performance targets met (<3s load, <500ms render)
- [ ] Screenshots captured and saved
- [ ] Code reviewed by Tony (Architect)
- [ ] QA passed by Heimdall
- [ ] Documentation updated

**Functional Requirements:**

- [ ] Map displays conflict events with correct severity colors
- [ ] Marker clustering works at low zoom levels
- [ ] Clicking markers opens popup with event details
- [ ] Keyboard navigation works (Tab, Enter, Space)
- [ ] Screen readers can access marker information
- [ ] Loading state shows while map initializes
- [ ] Error state shows if map fails to load
- [ ] Empty state shows when no events match filters
- [ ] Component cleans up properly on unmount

**Non-Functional Requirements:**

- [ ] No console errors (except expected HMR logs)
- [ ] No memory leaks (verified with DevTools)
- [ ] Bundle size <500KB (map-related code)
- [ ] TypeScript compilation succeeds with no errors
- [ ] ESLint passes with no warnings

---

## Dependencies

**Blockers:**
- None (can start immediately)

**Related Tasks:**
- Depends on: `docs/ARCH_MAP_COMPONENT.md` (completed)
- Blocks: Heimdall QA phase
- Related: Filter component implementation (future task)

---

## Resources

**Documentation:**
- `docs/ARCH_MAP_COMPONENT.md` - Architecture decision
- `docs/agent-workflow/REQ.md` - Requirements (FR-UI-1, FR-UI-2, NFR-ACC-1 through NFR-ACC-4)
- [Leaflet Documentation](https://leafletjs.com/)
- [Leaflet MarkerCluster](https://github.com/Leaflet/Leaflet.markercluster)

**Existing Code:**
- `frontend/app/components/ConflictMap.tsx` - Current implementation (review and refactor)
- `frontend/app/page.tsx` - Example of component usage

**Tools:**
- Chrome DevTools (performance profiling)
- axe-core or Lighthouse (accessibility audit)
- Jest + React Testing Library (unit tests)

---

## Notes

**From Architecture Review:**
- Leaflet is the correct choice for WarTracker (no WebGL dependency)
- Marker clustering is MANDATORY for scalability
- Accessibility is non-negotiable (WCAG 2.1 AA)
- OSM tiles are free and sufficient for MVP

**Known Issues:**
- Current implementation shows 38/50 events (12 have 0,0 coordinates)
- This is expected - filter invalid coordinates gracefully

**Future Enhancements (Not in Scope):**
- Heatmap layer
- Time-slider for historical playback
- Custom map styles (dark mode)
- Offline support

---

## Sign-Off

| Role | Name | Date | Status |
|------|------|------|--------|
| Architect | Tony | 2026-03-02 | ✅ Approved |
| Developer | Peter | Pending | ⏳ In Progress |
| QA | Heimdall | Pending | ⏳ Review |
| Coordinator | Jarvis | Pending | ⏳ Review |

---

**Document Location:** `docs/TASKS_MAP_FIX.md`  
**GitHub Issue:** (create if needed)  
**Estimated Completion:** 2026-03-03
