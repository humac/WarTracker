'use client'

import { useEffect, useRef, useState, useCallback } from 'react'

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
  if (severity >= 4) return '#dc2626'
  if (severity >= 3) return '#f59e0b'
  return '#22c55e'
}

const getClusterColor = (count: number): string => {
  if (count >= 100) return '#dc2626'
  if (count >= 50) return '#f59e0b'
  if (count >= 10) return '#eab308'
  return '#22c55e'
}

export function ConflictMap({ events, className, height = DEFAULT_HEIGHT, initialZoom = DEFAULT_ZOOM, initialCenter = DEFAULT_CENTER }: ConflictMapProps) {
  const mapRef = useRef<HTMLDivElement>(null)
  const [isLoaded, setIsLoaded] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    // Only load leaflet on client side
    let map: any = null
    let markerClusterGroup: any = null

    const initMap = async () => {
      try {
        // Dynamic imports for browser-only libraries
        const L = await import('leaflet')
        await import('leaflet.markercluster')

        if (!mapRef.current) return

        // Initialize map
        map = L.map(mapRef.current).setCenter(initialCenter, initialZoom)

        // Add tile layer
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
          attribution: '© OpenStreetMap contributors',
          maxZoom: 18,
        }).addTo(map)

        // Create marker cluster group
        markerClusterGroup = L.markerClusterGroup()

        // Add markers
        events.forEach((event) => {
          if (event.latitude && event.longitude) {
            const marker = L.marker([event.latitude, event.longitude])
            marker.bindPopup(`
              <strong>${event.title}</strong><br/>
              Severity: ${event.severity}<br/>
              Date: ${event.published_date}
            `)
            markerClusterGroup.addLayer(marker)
          }
        })

        map.addLayer(markerClusterGroup)
        setIsLoaded(true)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load map')
      }
    }

    initMap()

    return () => {
      if (map) {
        map.remove()
      }
    }
  }, [events, initialCenter, initialZoom])

  if (error) {
    return (
      <div className="flex items-center justify-center h-96 bg-muted/50 rounded-lg">
        <div className="text-center p-6 bg-red-50 dark:bg-red-900/20 rounded-lg">
          <svg className="w-12 h-12 mx-auto text-red-400 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <p className="text-red-800 dark:text-red-200 font-medium">{error}</p>
          <button
            onClick={() => typeof window !== 'undefined' && window.location.reload()}
            className="mt-4 px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors"
          >
            Refresh
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className={`relative ${className}`}>
      {!isLoaded && (
        <div className="flex items-center justify-center h-96 bg-muted/50 rounded-lg">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4" />
            <p className="text-muted-foreground">Loading map...</p>
          </div>
        </div>
      )}
      <div 
        ref={mapRef} 
        className={`rounded-lg overflow-hidden ${!isLoaded ? 'invisible' : ''}`}
        style={{ height }}
        aria-label="Interactive map showing conflict events worldwide"
        role="application"
      />
    </div>
  )
}
