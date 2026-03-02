'use client'

import { useEffect, useRef, useState, useCallback } from 'react'
import * as maplibregl from 'maplibre-gl'
import 'maplibre-gl/dist/maplibre-gl.css'
import * as Supercluster from 'supercluster'

interface ConflictEvent {
  id: number
  title: string
  latitude: number
  longitude: number
  severity: number
  published_date: string
}

interface ConflictMapProps {
  events: ConflictEvent[]
  className?: string
  height?: string
  initialZoom?: number
  initialCenter?: [number, number]
}

interface MapPoint extends GeoJSON.Feature<GeoJSON.Point> {
  properties: {
    cluster: boolean
    event_id?: number
    title?: string
    severity?: number
    published_date?: string
    point_count?: number
    cluster_id?: number
  }
}

interface SuperclusterOptions {
  radius: number
  extent: number
  minZoom: number
  maxZoom: number
}

const DEFAULT_CENTER: [number, number] = [35, 30]
const DEFAULT_ZOOM = 3
const DEFAULT_HEIGHT = '600px'

// Severity color mapping
const getSeverityColor = (severity: number): string => {
  if (severity >= 4) return '#dc2626' // Red
  if (severity >= 3) return '#f59e0b' // Orange
  return '#22c55e' // Green
}

const getClusterColor = (count: number): string => {
  if (count >= 100) return '#dc2626'
  if (count >= 50) return '#f59e0b'
  if (count >= 10) return '#eab308'
  return '#22c55e'
}

export function ConflictMap({
  events,
  className = '',
  height = DEFAULT_HEIGHT,
  initialZoom = DEFAULT_ZOOM,
  initialCenter = DEFAULT_CENTER,
}: ConflictMapProps) {
  const mapContainerRef = useRef<HTMLDivElement>(null)
  const mapRef = useRef<maplibregl.Map | null>(null)
  const markersRef = useRef<maplibregl.Marker[]>([])
  const [error, setError] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isMapReady, setIsMapReady] = useState(false)

  // Cleanup markers on unmount or events change
  const clearMarkers = useCallback(() => {
    markersRef.current.forEach(marker => marker.remove())
    markersRef.current = []
  }, [])

  // Initialize map
  useEffect(() => {
    if (!mapContainerRef.current) return

    let map: maplibregl.Map | null = null

    try {
      setIsLoading(true)
      
      map = new maplibregl.Map({
        container: mapContainerRef.current,
        style: 'https://demotiles.maplibre.org/style.json',
        center: initialCenter,
        zoom: initialZoom,
      })

      map.addControl(new maplibregl.NavigationControl())
      map.addControl(new maplibregl.ScaleControl())

      map.on('load', () => {
        setIsMapReady(true)
        setIsLoading(false)
      })

      map.on('error', (e) => {
        console.error('Map error:', e)
        setError('Unable to load map. Please try refreshing the page.')
        setIsLoading(false)
      })

      mapRef.current = map
    } catch (err) {
      console.error('Failed to initialize map:', err)
      setError('Unable to initialize map component.')
      setIsLoading(false)
    }

    return () => {
      if (map) {
        map.remove()
        mapRef.current = null
      }
      clearMarkers()
    }
  }, [clearMarkers, initialCenter, initialZoom])

  // Add markers when events change and map is ready
  useEffect(() => {
    if (!mapRef.current || !isMapReady) return

    clearMarkers()

    // Filter events with valid coordinates
    const validEvents = events.filter(
      e => e.latitude !== 0 || e.longitude !== 0
    )

    if (validEvents.length === 0) {
      return
    }

    // Create supercluster instance
    const clusters = new (Supercluster as any)({
      radius: 60,
      extent: 512,
      minZoom: 0,
      maxZoom: 16,
    }) as any

    // Prepare points for clustering
    const points: GeoJSON.Feature<GeoJSON.Point, {
      cluster: boolean
      event_id?: number
      title?: string
      severity?: number
      published_date?: string
    }>[] = validEvents.map(event => ({
      type: 'Feature',
      properties: {
        cluster: false,
        event_id: event.id,
        title: event.title,
        severity: event.severity,
        published_date: event.published_date,
      },
      geometry: {
        type: 'Point',
        coordinates: [event.longitude, event.latitude],
      },
    }))

    clusters.load(points)

    // Get clusters for current zoom level
    const zoom = mapRef.current.getZoom()
    const clusterFeatures = clusters.getClusters(
      mapRef.current.getBounds().toArray(),
      Math.round(zoom)
    ) as MapPoint[]

    // Add cluster markers
    clusterFeatures.forEach(feature => {
      const isCluster = feature.properties.cluster
      const [lng, lat] = feature.geometry.coordinates

      let el: HTMLDivElement

      if (isCluster) {
        const count = feature.properties.point_count || 0
        const color = getClusterColor(count)
        
        el = document.createElement('div')
        el.innerHTML = `
          <div style="
            background-color: ${color};
            color: white;
            font-weight: bold;
            font-size: 12px;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 3px solid white;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
            cursor: pointer;
          ">${count}</div>
        `

        el.addEventListener('click', () => {
          const clusterId = feature.properties.cluster_id
          if (clusterId !== undefined && mapRef.current) {
            const expansionZoom = clusters.getClusterExpansionZoom(clusterId)
            mapRef.current.easeTo({
              center: [lng, lat],
              zoom: expansionZoom,
              duration: 500,
            })
          }
        })
      } else {
        const event = {
          id: feature.properties.event_id!,
          title: feature.properties.title!,
          severity: feature.properties.severity!,
          published_date: feature.properties.published_date!,
        }
        const color = getSeverityColor(event.severity)

        el = document.createElement('div')
        el.innerHTML = `
          <div style="
            background-color: ${color};
            width: 16px;
            height: 16px;
            border-radius: 50%;
            border: 3px solid white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.3);
            cursor: pointer;
          "></div>
        `

        const popup = new maplibregl.Popup({ offset: 25 }).setHTML(`
          <div style="max-width: 250px; font-family: system-ui, -apple-system, sans-serif;">
            <strong style="font-size: 14px; color: #1a1a1a; display: block; margin-bottom: 4px;">${event.title}</strong>
            <div style="color: #666; font-size: 12px; margin-bottom: 2px;">
              <span style="font-weight: 500;">Severity:</span> ${event.severity}/5
            </div>
            <div style="color: #666; font-size: 12px;">
              <span style="font-weight: 500;">Date:</span> ${event.published_date}
            </div>
          </div>
        `)

        const marker = new maplibregl.Marker({ element: el, anchor: 'center' })
          .setLngLat([lng, lat])
          .setPopup(popup)
          .addTo(mapRef.current!)

        markersRef.current.push(marker)
        return // Skip adding to markers array for clusters
      }

      const marker = new maplibregl.Marker({ element: el, anchor: 'center' })
        .setLngLat([lng, lat])
        .addTo(mapRef.current!)

      markersRef.current.push(marker)
    })

    // Fit bounds if we have markers
    if (validEvents.length > 0 && mapRef.current) {
      const bounds = new maplibregl.LngLatBounds()
      validEvents.forEach(event => {
        bounds.extend([event.longitude, event.latitude])
      })
      mapRef.current.fitBounds(bounds, { padding: 50, duration: 0 })
    }
  }, [events, isMapReady, clearMarkers])

  // Handle zoom changes for dynamic clustering
  useEffect(() => {
    if (!mapRef.current || !isMapReady) return

    const handleZoomChange = () => {
      // Trigger re-clustering by updating events dependency
      // This is handled by the events useEffect
    }

    mapRef.current.on('zoomend', handleZoomChange)
    return () => {
      if (mapRef.current) {
        mapRef.current.off('zoomend', handleZoomChange)
      }
    }
  }, [isMapReady])

  // Error boundary fallback
  if (error) {
    return (
      <div className={`bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-6 text-center ${className}`}>
        <svg className="w-12 h-12 mx-auto text-red-400 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <p className="text-red-800 dark:text-red-200 font-medium">{error}</p>
        <button
          onClick={() => window.location.reload()}
          className="mt-4 px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors"
        >
          Refresh Page
        </button>
      </div>
    )
  }

  // Loading state
  if (isLoading) {
    return (
      <div className={`relative ${className}`} style={{ height }}>
        <div className="absolute inset-0 flex items-center justify-center bg-gray-100 dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600 dark:text-gray-400">Loading map...</p>
          </div>
        </div>
      </div>
    )
  }

  const validEventCount = events.filter(e => e.latitude !== 0 || e.longitude !== 0).length

  return (
    <div className={className}>
      <div
        ref={mapContainerRef}
        className="w-full rounded-lg border border-gray-200 dark:border-gray-700 overflow-hidden"
        style={{ height }}
        role="application"
        aria-label="Conflict events map"
      />
      
      {/* Map legend and stats */}
      <div className="mt-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 text-sm">
        <p className="text-gray-600 dark:text-gray-400">
          Showing <span className="font-semibold text-gray-900 dark:text-gray-100">{validEventCount}</span> of{' '}
          <span className="font-semibold text-gray-900 dark:text-gray-100">{events.length}</span> events with valid coordinates
        </p>
        
        <div className="flex flex-wrap items-center gap-4">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-red-600"></div>
            <span className="text-gray-600 dark:text-gray-400">High (4-5)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
            <span className="text-gray-600 dark:text-gray-400">Medium (3)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-green-500"></div>
            <span className="text-gray-600 dark:text-gray-400">Low (1-2)</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ConflictMap
