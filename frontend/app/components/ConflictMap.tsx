'use client'

import { useEffect, useRef, useState, useCallback } from 'react'
import * as L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import 'leaflet.markercluster'
import 'leaflet.markercluster/dist/MarkerCluster.css'
import 'leaflet.markercluster/dist/MarkerCluster.Default.css'

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

// Custom cluster icon factory
const createClusterIcon = (count: number): L.DivIcon => {
  const color = getClusterColor(count)
  return L.divIcon({
    html: `
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
      " aria-label="Cluster of ${count} events"
      role="button"
      tabindex="0">
        ${count}
      </div>
    `,
    className: 'custom-cluster-icon',
    iconSize: [32, 32],
    iconAnchor: [16, 16],
  })
}

// Custom marker icon factory
const createMarkerIcon = (severity: number): L.DivIcon => {
  const color = getSeverityColor(severity)
  return L.divIcon({
    html: `
      <div style="
        background-color: ${color};
        width: 16px;
        height: 16px;
        border-radius: 50%;
        border: 3px solid white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
        cursor: pointer;
      " aria-label="Conflict event marker"
      role="button"
      tabindex="0">
        <span class="visually-hidden">Severity ${severity}</span>
      </div>
    `,
    className: 'custom-marker-icon',
    iconSize: [16, 16],
    iconAnchor: [8, 8],
  })
}

export function ConflictMap({
  events,
  className = '',
  height = DEFAULT_HEIGHT,
  initialZoom = DEFAULT_ZOOM,
  initialCenter = DEFAULT_CENTER,
}: ConflictMapProps) {
  const mapContainerRef = useRef<HTMLDivElement>(null)
  const mapRef = useRef<L.Map | null>(null)
  const clusterGroupRef = useRef<L.MarkerClusterGroup | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isMapReady, setIsMapReady] = useState(false)
  const [mapLoadTimeout, setMapLoadTimeout] = useState(false)

  // Cleanup on unmount
  const cleanup = useCallback(() => {
    if (clusterGroupRef.current) {
      clusterGroupRef.current.clearLayers()
      clusterGroupRef.current = null
    }
    if (mapRef.current) {
      mapRef.current.remove()
      mapRef.current = null
    }
  }, [])

  // Initialize map
  useEffect(() => {
    if (!mapContainerRef.current) return

    let map: L.Map | null = null
    let loadTimeout: NodeJS.Timeout | null = null

    try {
      setIsLoading(true)
      
      // Create map instance
      map = L.map(mapContainerRef.current, {
        center: initialCenter,
        zoom: initialZoom,
        zoomControl: true,
        attributionControl: true,
      })

      // Add tile layer (OpenStreetMap)
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 18,
      }).addTo(map)

      // Add zoom control with keyboard support
      L.control.zoom({
        position: 'topright',
      }).addTo(map)

      // Handle map load
      map.whenReady(() => {
        setIsMapReady(true)
        setIsLoading(false)
        if (loadTimeout) {
          clearTimeout(loadTimeout)
        }
      })

      // Handle map errors
      map.on('error', (e: any) => {
        console.error('Map error:', e)
        setError('Unable to load map. Please try refreshing the page.')
        setIsLoading(false)
        if (loadTimeout) {
          clearTimeout(loadTimeout)
        }
      })

      // Timeout for map initialization (prevent infinite loading)
      loadTimeout = setTimeout(() => {
        if (isLoading) {
          console.warn('Map initialization timeout')
          setMapLoadTimeout(true)
          setError('Map loading is taking longer than expected. Please try refreshing.')
          setIsLoading(false)
        }
      }, 10000) // 10 second timeout

      mapRef.current = map
    } catch (err) {
      console.error('Failed to initialize map:', err)
      setError('Unable to initialize map component.')
      setIsLoading(false)
      if (loadTimeout) {
        clearTimeout(loadTimeout)
      }
    }

    return () => {
      if (loadTimeout) {
        clearTimeout(loadTimeout)
      }
      cleanup()
    }
  }, [cleanup, initialCenter, initialZoom, isLoading])

  // Add markers when events change and map is ready
  useEffect(() => {
    if (!mapRef.current || !isMapReady) return

    // Clear existing cluster group
    if (clusterGroupRef.current) {
      clusterGroupRef.current.clearLayers()
      mapRef.current.removeLayer(clusterGroupRef.current)
    }

    // Filter events with valid coordinates
    const validEvents = events.filter(
      e => (e.latitude !== 0 && e.latitude !== null) || (e.longitude !== 0 && e.longitude !== null)
    )

    if (validEvents.length === 0) {
      return
    }

    // Create marker cluster group
    const clusterGroup = L.markerClusterGroup({
      maxClusterRadius: 50,
      disableClusteringAtZoom: 10,
      spiderfyOnMaxZoom: true,
      showCoverageOnHover: true,
      removeOutsideVisibleBounds: true,
    })

    // Add markers
    validEvents.forEach(event => {
      const icon = createMarkerIcon(event.severity)
      const marker = L.marker([event.latitude, event.longitude], { icon })

      // Create popup content
      const popupContent = `
        <div style="max-width: 250px; font-family: system-ui, -apple-system, sans-serif;">
          <strong style="font-size: 14px; color: #1a1a1a; display: block; margin-bottom: 4px;">${event.title}</strong>
          <div style="color: #666; font-size: 12px; margin-bottom: 2px;">
            <span style="font-weight: 500;">Severity:</span> ${event.severity}/5
          </div>
          <div style="color: #666; font-size: 12px;">
            <span style="font-weight: 500;">Date:</span> ${event.published_date}
          </div>
        </div>
      `

      marker.bindPopup(popupContent)

      // Add keyboard support for markers
      const markerElement = marker.getElement()
      if (markerElement) {
        markerElement.setAttribute('role', 'button')
        markerElement.setAttribute('tabindex', '0')
        markerElement.setAttribute('aria-label', `Conflict event: ${event.title}, Severity ${event.severity}`)
        
        markerElement.addEventListener('keydown', (e: KeyboardEvent) => {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault()
            marker.openPopup()
          }
        })
      }

      clusterGroup.addLayer(marker)
    })

    // Add cluster group to map
    mapRef.current.addLayer(clusterGroup)
    clusterGroupRef.current = clusterGroup

    // Fit bounds to show all markers
    if (validEvents.length > 0 && mapRef.current) {
      const group = L.featureGroup(
        validEvents.map(event => L.marker([event.latitude, event.longitude]))
      )
      mapRef.current.fitBounds(group.getBounds(), { padding: [50, 50] })
    }
  }, [events, isMapReady])

  // Error boundary fallback
  if (error) {
    return (
      <div 
        className={`bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-6 text-center ${className}`}
        role="alert"
        aria-live="assertive"
      >
        <svg className="w-12 h-12 mx-auto text-red-400 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <p className="text-red-800 dark:text-red-200 font-medium">{error}</p>
        <button
          onClick={() => window.location.reload()}
          className="mt-4 px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2"
          aria-label="Refresh page"
        >
          Refresh Page
        </button>
      </div>
    )
  }

  // Loading state
  if (isLoading) {
    return (
      <div className={`relative ${className}`} style={{ height }} role="status" aria-live="polite">
        <div className="absolute inset-0 flex items-center justify-center bg-gray-100 dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4" aria-hidden="true"></div>
            <p className="text-gray-600 dark:text-gray-400">Loading map...</p>
            {mapLoadTimeout && (
              <p className="text-yellow-600 dark:text-yellow-400 text-sm mt-2">
                This is taking longer than expected...
              </p>
            )}
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
        aria-label="Conflict events map showing global incidents with severity markers"
        tabIndex={0}
      />
      
      {/* Map legend and stats */}
      <div className="mt-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 text-sm" role="region" aria-label="Map legend">
        <p className="text-gray-600 dark:text-gray-400">
          Showing <span className="font-semibold text-gray-900 dark:text-gray-100">{validEventCount}</span> of{' '}
          <span className="font-semibold text-gray-900 dark:text-gray-100">{events.length}</span> events with valid coordinates
        </p>
        
        <div className="flex flex-wrap items-center gap-4">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-red-600" aria-hidden="true"></div>
            <span className="text-gray-600 dark:text-gray-400">High (4-5)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-yellow-500" aria-hidden="true"></div>
            <span className="text-gray-600 dark:text-gray-400">Medium (3)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-green-500" aria-hidden="true"></div>
            <span className="text-gray-600 dark:text-gray-400">Low (1-2)</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ConflictMap
