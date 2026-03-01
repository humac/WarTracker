'use client';

import { useEffect, useRef, useState } from 'react';
import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';

interface ConflictEvent {
  id: number;
  title: string;
  latitude: number;
  longitude: number;
  severity: number;
  published_date: string;
}

export function ConflictMap({ events = [] }: { events: ConflictEvent[] }) {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<maplibregl.Map | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!mapContainer.current) return;

    try {
      map.current = new maplibregl.Map({
        container: mapContainer.current,
        style: 'https://demotiles.maplibre.org/style.json',
        center: [35, 30],
        zoom: 3
      });

      map.current.on('load', () => setLoading(false));
      map.current.on('error', (e) => {
        console.error('Map error:', e);
        setError('Unable to load map. WebGL may not be supported.');
        setLoading(false);
      });
    } catch (err) {
      console.error('Failed to initialize map:', err);
      setError('Unable to initialize map. WebGL may not be supported.');
      setLoading(false);
    }

    return () => map.current?.remove();
  }, []);

  useEffect(() => {
    if (!map.current || events.length === 0) return;

    // Add markers for events
    events.forEach(event => {
      const el = document.createElement('div');
      el.className = 'marker';
      el.style.backgroundColor = event.severity >= 4 ? '#dc2626' : event.severity >= 3 ? '#f59e0b' : '#22c55e';
      el.style.width = '12px';
      el.style.height = '12px';
      el.style.borderRadius = '50%';
      el.style.border = '2px solid white';
      el.style.cursor = 'pointer';
      
      const popup = new maplibregl.Popup({ offset: 1 }).setHTML(
        `<strong>${event.title}</strong><br/>Severity: ${event.severity}<br/>Date: ${event.published_date}`
      );

      new maplibregl.Marker({ element: el })
        .setLngLat([event.longitude, event.latitude])
        .setPopup(popup)
        .addTo(map.current!);
    });
  }, [events]);

  if (error) {
    return (
      <div className="relative w-full h-[600px] bg-gray-100 dark:bg-gray-800 rounded-lg flex items-center justify-center">
        <div className="text-center p-8">
          <div className="text-6xl mb-4">🗺️</div>
          <h3 className="text-xl font-semibold text-gray-800 dark:text-gray-200 mb-2">Map Unavailable</h3>
          <p className="text-gray-600 dark:text-gray-400 mb-4">{error}</p>
          <div className="text-sm text-gray-500 dark:text-gray-500">
            <p>Showing {events.length} conflict events:</p>
            <ul className="mt-2 space-y-1 max-h-48 overflow-y-auto">
              {events.map(event => (
                <li key={event.id} className="text-left">
                  <span className={`inline-block w-3 h-3 rounded-full mr-2 ${
                    event.severity >= 4 ? 'bg-red-600' : event.severity >= 3 ? 'bg-yellow-500' : 'bg-green-500'
                  }`}></span>
                  {event.title} ({event.latitude.toFixed(2)}, {event.longitude.toFixed(2)})
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="relative w-full h-[600px] rounded-lg overflow-hidden">
      {loading && (
        <div className="absolute inset-0 flex items-center justify-center bg-gray-100 dark:bg-gray-800">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-4 text-gray-600 dark:text-gray-400">Loading map...</p>
          </div>
        </div>
      )}
      <div ref={mapContainer} className="w-full h-full" />
    </div>
  );
}
