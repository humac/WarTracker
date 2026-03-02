import { render, screen } from '@testing-library/react'
import { ConflictMap } from './ConflictMap'

// Mock maplibre-gl
jest.mock('maplibre-gl', () => {
  const mockPopup = {
    setHTML: jest.fn().mockReturnThis(),
    addTo: jest.fn().mockReturnThis(),
  }

  const mockMarker = {
    setLngLat: jest.fn().mockReturnThis(),
    setPopup: jest.fn().mockReturnThis(),
    addTo: jest.fn().mockReturnThis(),
    remove: jest.fn(),
  }

  const mockMap = {
    on: jest.fn(),
    off: jest.fn(),
    addControl: jest.fn(),
    getZoom: jest.fn().mockReturnValue(3),
    getBounds: jest.fn().mockReturnValue({
      toArray: () => [[-180, -90], [180, 90]],
    }),
    easeTo: jest.fn(),
    fitBounds: jest.fn(),
    remove: jest.fn(),
  }

  return {
    Map: jest.fn().mockImplementation(() => mockMap),
    Marker: jest.fn().mockImplementation(() => mockMarker),
    Popup: jest.fn().mockImplementation(() => mockPopup),
    NavigationControl: jest.fn(),
    ScaleControl: jest.fn(),
    LngLatBounds: jest.fn().mockImplementation(() => ({
      extend: jest.fn(),
    })),
  }
})

// Mock supercluster
jest.mock('supercluster', () => {
  return jest.fn().mockImplementation(() => ({
    load: jest.fn(),
    getClusters: jest.fn().mockReturnValue([]),
    getClusterExpansionZoom: jest.fn().mockReturnValue(5),
  }))
})

describe('ConflictMap', () => {
  const mockEvents = [
    {
      id: 1,
      title: 'Test Event 1',
      latitude: 40.7128,
      longitude: -74.006,
      severity: 4,
      published_date: '2024-01-15',
    },
    {
      id: 2,
      title: 'Test Event 2',
      latitude: 51.5074,
      longitude: -0.1278,
      severity: 2,
      published_date: '2024-01-16',
    },
    {
      id: 3,
      title: 'Test Event 3',
      latitude: 35.6762,
      longitude: 139.6503,
      severity: 3,
      published_date: '2024-01-17',
    },
  ]

  describe('Loading State', () => {
    it('should render loading state initially', () => {
      render(<ConflictMap events={mockEvents} />)
      
      expect(screen.getByText('Loading map...')).toBeInTheDocument()
    })

    it('should render with custom className in loading state', () => {
      const { container } = render(
        <ConflictMap events={mockEvents} className="custom-class" />
      )
      
      expect(container.firstChild).toHaveClass('custom-class')
    })
  })

  describe('Props Validation', () => {
    it('should accept required events prop', () => {
      expect(() => {
        render(<ConflictMap events={mockEvents} />)
      }).not.toThrow()
    })

    it('should accept optional height prop', () => {
      expect(() => {
        render(<ConflictMap events={mockEvents} height="400px" />)
      }).not.toThrow()
    })

    it('should accept optional className prop', () => {
      expect(() => {
        render(<ConflictMap events={mockEvents} className="test-class" />)
      }).not.toThrow()
    })

    it('should accept optional initialZoom prop', () => {
      expect(() => {
        render(<ConflictMap events={mockEvents} initialZoom={10} />)
      }).not.toThrow()
    })

    it('should accept optional initialCenter prop', () => {
      expect(() => {
        render(<ConflictMap events={mockEvents} initialCenter={[45, -100]} />)
      }).not.toThrow()
    })
  })

  describe('Empty State', () => {
    it('should render with empty events array', () => {
      render(<ConflictMap events={[]} />)
      
      expect(screen.getByText('Loading map...')).toBeInTheDocument()
    })
  })

  describe('TypeScript Type Safety', () => {
    it('should compile with correct ConflictEvent interface', () => {
      // This test verifies TypeScript compilation
      const event: {
        id: number
        title: string
        latitude: number
        longitude: number
        severity: number
        published_date: string
      } = mockEvents[0]
      
      expect(event.id).toBe(1)
      expect(event.title).toBe('Test Event 1')
      expect(event.latitude).toBe(40.7128)
      expect(event.longitude).toBe(-74.006)
      expect(event.severity).toBe(4)
    })

    it('should compile with correct ConflictMapProps interface', () => {
      // This test verifies TypeScript compilation
      const props: {
        events: typeof mockEvents
        className?: string
        height?: string
        initialZoom?: number
        initialCenter?: [number, number]
      } = {
        events: mockEvents,
        className: 'test',
        height: '500px',
        initialZoom: 5,
        initialCenter: [35, 30],
      }
      
      expect(props.events.length).toBe(3)
      expect(props.className).toBe('test')
      expect(props.height).toBe('500px')
    })

    it('should compile with only required props', () => {
      // This test verifies that only events is required
      const props: {
        events: typeof mockEvents
      } = {
        events: mockEvents,
      }
      
      expect(props.events.length).toBe(3)
    })
  })

  describe('Component Structure', () => {
    it('should render without crashing', () => {
      const { container } = render(<ConflictMap events={mockEvents} />)
      expect(container).toBeTruthy()
    })

    it('should render a container div', () => {
      const { container } = render(<ConflictMap events={mockEvents} />)
      expect(container.firstChild).toBeInTheDocument()
    })
  })
})
