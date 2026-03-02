# Architecture Decision: Map Component

**Project:** WarTracker  
**Document ID:** ARCH-MAP-001  
**Date:** 2026-03-02  
**Author:** Tony (Architect)  
**Status:** ✅ Approved

---

## Executive Summary

**Decision:** Use **Leaflet.js** as the primary mapping library for WarTracker.

**Rationale:** Leaflet provides optimal balance of performance, compatibility, and feature set for WarTracker's use case (marker-based conflict visualization with 1,000-10,000 events). WebGL-dependent libraries (MapLibre GL) are unnecessary overhead.

---

## Context

### Problem Statement

WarTracker requires an interactive map to display global conflict events with:
- Color-coded severity markers (1-5 scale)
- Clickable popups with event details
- Filter controls (type, severity, date range)
- Support for 1,000-10,000 concurrent markers
- Universal browser compatibility (including older devices)

### Initial Implementation

Jarvis initially implemented MapLibre GL, then switched to Leaflet.js without architectural review. This document validates that decision and provides implementation guidance.

---

## Options Considered

### Option 1: Leaflet.js (RECOMMENDED) ✅

**Description:** Mature, lightweight 2D mapping library (est. 2010)

**Pros:**
- ✅ **No WebGL required** - Works on all browsers, including older devices
- ✅ **Lightweight** - ~400KB gzipped (vs 1MB+ for WebGL libraries)
- ✅ **Simple API** - Easy to implement and maintain
- ✅ **Excellent marker clustering** - Leaflet.markercluster plugin mature and performant
- ✅ **Universal browser support** - Critical for journalists/NGOs in low-resource environments
- ✅ **Large ecosystem** - Extensive plugin library
- ✅ **Stable API** - Minimal breaking changes since v1.0

**Cons:**
- ❌ No 3D terrain or pitch/rotation controls
- ❌ Canvas-based rendering (slower than WebGL for 100,000+ markers)
- ❌ Limited vector tile styling capabilities
- ❌ No built-in 3D buildings or terrain visualization

**Best For:**
- Marker-based visualization (our use case)
- Applications prioritizing compatibility over advanced features
- Teams with limited frontend mapping expertise

### Option 2: MapLibre GL

**Description:** WebGL-powered vector map library (Mapbox GL fork)

**Pros:**
- ✅ **Hardware accelerated** - Better performance for 100,000+ markers
- ✅ **3D terrain & buildings** - Immersive visualization
- ✅ **Vector tiles** - Dynamic styling, smaller tile payloads
- ✅ **Smooth zoom/pan** - GPU-accelerated rendering
- ✅ **Advanced effects** - Heatmaps, 3D extrusions, custom shaders

**Cons:**
- ❌ **Requires WebGL** - Fails on older browsers, some mobile devices, VMs
- ❌ **Larger bundle** - ~1MB+ gzipped
- ❌ **Complex API** - Steeper learning curve
- ❌ **Marker clustering less mature** - Requires custom implementation or third-party libs
- ❌ **Overkill for our use case** - We don't need 3D/terrain features

**Best For:**
- Data visualization requiring 3D/terrain
- Applications with 100,000+ data points
- Modern browser-only environments
- Custom map styling requirements

### Option 3: MapLibre GL with Leaflet Fallback

**Description:** Use MapLibre GL for modern browsers, fallback to Leaflet for others

**Pros:**
- ✅ Best of both worlds (advanced features + compatibility)
- ✅ Graceful degradation

**Cons:**
- ❌ **Double maintenance** - Two codepaths to test and maintain
- ❌ **Increased bundle size** - Both libraries included
- ❌ **Feature inconsistency** - Users on different browsers see different UI
- ❌ **Complexity** - Feature detection, state synchronization

**Best For:**
- Applications where 3D features are core to UX
- Teams with resources to maintain dual implementations

---

## Decision Matrix

| Criteria | Weight | Leaflet | MapLibre GL | Hybrid |
|----------|--------|---------|-------------|--------|
| **Browser Compatibility** | High (3x) | ✅ 10 | ❌ 4 | ✅ 10 |
| **Performance (1K-10K markers)** | High (3x) | ✅ 9 | ✅ 9 | ✅ 9 |
| **Bundle Size** | Medium (2x) | ✅ 9 | ❌ 5 | ❌ 4 |
| **Marker Clustering** | High (3x) | ✅ 10 | ❌ 6 | ✅ 10 |
| **3D/Terrain Features** | Low (1x) | ❌ 3 | ✅ 10 | ✅ 10 |
| **Implementation Complexity** | Medium (2x) | ✅ 10 | ❌ 5 | ❌ 3 |
| **Maintenance Burden** | Medium (2x) | ✅ 10 | ✅ 8 | ❌ 4 |
| **Ecosystem/Plugins** | Medium (2x) | ✅ 10 | ✅ 8 | ✅ 10 |
| **Weighted Score** | | **9.4** | **6.6** | **7.8** |

**Scoring:** 1-10 scale (10 = best fit for WarTracker)

---

## Recommended Architecture

### Primary Library: Leaflet.js

**Version:** `^1.9.4` (current stable)

**Dependencies:**
```json
{
  "leaflet": "^1.9.4",
  "@types/leaflet": "^1.9.21",
  "@types/leaflet.markercluster": "^1.5.4"
}
```

### Marker Clustering Strategy

**Plugin:** `@types/leaflet.markercluster` + `leaflet.markercluster`

**Rationale:**
- Handles 10,000+ markers efficiently
- Automatic clustering based on zoom level
- Customizable cluster icons (color-coded by severity)
- Smooth animations

**Implementation:**
```typescript
import L from 'leaflet'
import 'leaflet.markercluster'
import 'leaflet.markercluster/dist/MarkerCluster.css'
import 'leaflet.markercluster/dist/MarkerCluster.Default.css'

const clusterGroup = L.markerClusterGroup({
  maxClusterRadius: 50,
  disableClusteringAtZoom: 10,
  spiderfyOnMaxZoom: true,
  showCoverageOnHover: true,
})

// Add markers
events.forEach(event => {
  const marker = L.marker([event.latitude, event.longitude])
  clusterGroup.addLayer(marker)
})

map.addLayer(clusterGroup)
```

### Tile Provider Recommendation

**Primary:** OpenStreetMap (OSM) - Free, no API key required

```typescript
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap contributors',
  maxZoom: 18,
})
```

**Alternative (Production):** MapTiler - Better performance, custom styling

```typescript
L.tileLayer('https://api.maptiler.com/maps/streets/{z}/{x}/{y}.png?key={apiKey}', {
  attribution: '© MapTiler',
  maxZoom: 18,
})
```

**Comparison:**

| Provider | Cost | API Key | Performance | Customization |
|----------|------|---------|-------------|---------------|
| OpenStreetMap | Free | ❌ No | Good | Limited |
| MapTiler | Freemium | ✅ Yes | Excellent | High |
| Stadia Maps | Freemium | ✅ Yes | Excellent | High |
| CartoDB | Freemium | ✅ Yes | Excellent | Medium |

**Recommendation:** Start with OSM (no API key required), migrate to MapTiler if performance/customization needs arise.

---

## Performance Considerations

### Marker Rendering

**Target:** 1,000-10,000 markers with <100ms interaction latency

**Optimization Strategies:**

1. **Marker Clustering** (MANDATORY)
   - Cluster markers at low zoom levels
   - Disable clustering at zoom ≥10
   - Use `maxClusterRadius: 50` for optimal grouping

2. **Virtual Scrolling** (for 10,000+ markers)
   - Only render markers in viewport
   - Use `leaflet-canvaslayer-field` for canvas rendering

3. **Lazy Loading**
   - Load markers for visible region first
   - Fetch additional markers on map move (debounced)

4. **Icon Optimization**
   - Use `L.divIcon` for custom markers (lighter than images)
   - Pre-render icons as data URIs
   - Avoid per-marker DOM manipulation

### Memory Management

**Target:** <100MB memory usage with 10,000 markers

**Strategies:**
- Remove off-screen markers (virtual scrolling)
- Reuse marker objects when possible
- Clear cluster groups before re-rendering
- Use `map.remove()` on component unmount

### Bundle Size Optimization

**Target:** <500KB total map-related bundle

**Strategies:**
- Tree-shake Leaflet imports
- Lazy-load map component (Next.js dynamic import)
- Use CDN for Leaflet CSS (optional)

```typescript
// Lazy-load map component
const ConflictMap = dynamic(() => import('./components/ConflictMap'), {
  ssr: false, // Leaflet requires window object
  loading: () => <MapSkeleton />
})
```

---

## Accessibility Requirements

### WCAG 2.1 AA Compliance

**Requirements:**

1. **Keyboard Navigation**
   - All map controls accessible via Tab/Enter
   - Arrow keys to pan map
   - +/- keys to zoom

2. **Screen Reader Support**
   - ARIA labels on all markers
   - Descriptive text for cluster counts
   - Announce map updates (live regions)

3. **Color Independence**
   - Severity indicated by icons + colors (not color alone)
   - High contrast markers (border + fill)
   - Pattern fills for colorblind users (optional)

4. **Focus Management**
   - Visible focus indicators on markers
   - Focus trap in popups
   - Return focus on popup close

**Implementation Example:**
```typescript
const icon = L.divIcon({
  className: 'custom-marker',
  html: `
    <div 
      role="button" 
      aria-label="Conflict event: ${event.title}, Severity ${event.severity}"
      tabindex="0"
      style="..."
    >
      <span class="visually-hidden">Severity ${event.severity}</span>
    </div>
  `,
})

marker.on('keydown', (e) => {
  if (e.key === 'Enter' || e.key === ' ') {
    marker.openPopup()
  }
})
```

---

## Implementation Guidelines

### Component Structure

```
frontend/app/components/
├── ConflictMap.tsx          # Main map component
├── ConflictMap.types.ts     # TypeScript interfaces
├── ConflictMap.hooks.ts     # Custom hooks (useMapEvents, etc.)
├── MapMarkers/
│   ├── SeverityMarker.tsx   # Individual marker component
│   ├── ClusterIcon.tsx      # Custom cluster icon
│   └── index.ts
├── MapControls/
│   ├── FilterControl.tsx    # Filter UI
│   ├── LegendControl.tsx    # Severity legend
│   └── index.ts
└── index.ts
```

### State Management

**Use Zustand for map state:**
```typescript
interface MapState {
  filters: FilterOptions
  selectedEvent: ConflictEvent | null
  viewport: Viewport
  setFilters: (filters: FilterOptions) => void
  setSelectedEvent: (event: ConflictEvent | null) => void
}

export const useMapStore = create<MapState>((set) => ({
  filters: defaultFilters,
  selectedEvent: null,
  viewport: defaultViewport,
  setFilters: (filters) => set({ filters }),
  setSelectedEvent: (event) => set({ selectedEvent: event }),
}))
```

### Error Handling

**Graceful Degradation:**
```typescript
const [error, setError] = useState<string | null>(null)

useEffect(() => {
  try {
    // Initialize map
  } catch (err) {
    console.error('Map initialization failed:', err)
    setError('Unable to load map. Showing list view instead.')
  }
}, [])

if (error) {
  return <EventList events={events} /> // Fallback UI
}
```

**Loading States:**
```typescript
const [isLoading, setIsLoading] = useState(true)

return (
  <>
    {isLoading && <MapSkeleton />}
    <div ref={mapContainerRef} className={isLoading ? 'hidden' : 'block'} />
  </>
)
```

---

## Testing Strategy

### Unit Tests

**Coverage Targets:**
- Component rendering: 100%
- Marker creation: 100%
- Cluster logic: 100%
- Filter application: 100%

**Test Examples:**
```typescript
describe('ConflictMap', () => {
  it('renders map container', () => {
    render(<ConflictMap events={mockEvents} />)
    expect(screen.getByTestId('map-container')).toBeInTheDocument()
  })

  it('creates markers for valid events', () => {
    render(<ConflictMap events={mockEvents} />)
    expect(screen.getAllByRole('button', { name: /conflict event/i })).toHaveLength(
      mockEvents.filter(e => e.latitude !== 0).length
    )
  })

  it('clusters markers at low zoom', async () => {
    render(<ConflictMap events={largeEventSet} />)
    const clusters = await screen.findAllByTestId('marker-cluster')
    expect(clusters.length).toBeLessThan(largeEventSet.length)
  })
})
```

### Integration Tests

**Test Scenarios:**
1. Map loads with events from API
2. Clicking marker opens popup with correct data
3. Filters update marker visibility
4. Clustering works at different zoom levels
5. Keyboard navigation works

### Browser Testing

**Required Browsers:**
- Chrome (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)
- Edge (latest 2 versions)
- Mobile Safari (iOS 14+)
- Chrome Mobile (Android 10+)

**Testing Checklist:**
- [ ] Map renders correctly
- [ ] Markers display with correct colors
- [ ] Popups open/close properly
- [ ] Clustering works
- [ ] Filters apply correctly
- [ ] Keyboard navigation works
- [ ] Touch gestures work (mobile)
- [ ] No console errors

---

## Migration from MapLibre GL

**If migrating from MapLibre GL to Leaflet:**

1. **Update dependencies:**
   ```bash
   npm uninstall maplibre-gl react-map-gl
   npm install leaflet @types/leaflet leaflet.markercluster @types/leaflet.markercluster
   ```

2. **Update imports:**
   ```typescript
   // Before (MapLibre)
   import Map, { Marker } from 'react-map-gl'
   
   // After (Leaflet)
   import L from 'leaflet'
   import { useEffect, useRef } from 'react'
   ```

3. **Update component structure:**
   - Replace `<Map>` with `<div ref={mapContainerRef}>`
   - Replace `<Marker>` with `L.marker().addTo(map)`
   - Update coordinate format: `[lat, lng]` (Leaflet) vs `[lng, lat]` (MapLibre)

4. **Update tile layers:**
   - MapLibre uses vector tiles (MapTiler, etc.)
   - Leaflet uses raster tiles (OSM, etc.)

5. **Test thoroughly:**
   - Verify all markers render
   - Test clustering
   - Check popup functionality
   - Verify filters work

---

## Future Considerations

### When to Reconsider MapLibre GL

Revisit this decision if:
- WarTracker needs 3D terrain visualization
- Marker count exceeds 100,000
- Vector tile styling becomes a requirement
- User research shows demand for 3D/immersive views

### Planned Enhancements (Leaflet)

**Q2 2026:**
- Heatmap layer for conflict density
- Time-slider for historical playback
- Custom map styles (dark mode, high contrast)

**Q3 2026:**
- Offline map support (service worker + tile caching)
- Draw tools for user annotations (future feature)

---

## References

- [Leaflet Documentation](https://leafletjs.com/)
- [Leaflet MarkerCluster](https://github.com/Leaflet/Leaflet.markercluster)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Map Tile Providers Comparison](https://leafletjs.com/plugins.html#tile-providers)

---

## Approval

| Role | Name | Date | Status |
|------|------|------|--------|
| Architect | Tony | 2026-03-02 | ✅ Approved |
| Developer | Peter | Pending | ⏳ Review |
| QA | Heimdall | Pending | ⏳ Review |
| Coordinator | Jarvis | Pending | ⏳ Review |

---

**Document Location:** `docs/ARCH_MAP_COMPONENT.md`  
**Next Review:** 2026-06-02 (quarterly)
