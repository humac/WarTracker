'use client'

import { useEffect, useState } from 'react'
// Force dynamic rendering - this page requires browser APIs
export const dynamic = 'force-dynamic'
export const ssr = true
import { ConflictMap } from './components/ConflictMap'
import { Timeline } from './components/Timeline'
import { Alerts } from './components/Alerts'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Skeleton } from '@/components/ui/skeleton'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { NavigationMenu, NavigationMenuItem, NavigationMenuLink, NavigationMenuList, navigationMenuTriggerStyle } from '@/components/ui/navigation-menu'
import { cn } from '@/lib/utils'
import { Loader2 } from 'lucide-react'

interface ConflictEvent {
  id: number
  title: string
  latitude: number
  longitude: number
  severity: number
  published_date: string
  country_code?: string
}

type Tab = 'map' | 'timeline' | 'alerts'


export default function Home() {
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [events, setEvents] = useState<ConflictEvent[]>([])
  const [activeTab, setActiveTab] = useState<Tab>('map')
  const [isFetching, setIsFetching] = useState(false)
  const [fetchResult, setFetchResult] = useState<{status: string, count: number} | null>(null)

  const handleFetchData = async () => {
    setIsFetching(true)
    setFetchResult(null)
    try {
      const response = await fetch('/api/v1/collect/gdelt', {
        method: 'POST',
        headers: {
          'Cache-Control': 'no-cache',
          'Pragma': 'no-cache',
        },
      })
      const data = await response.json()
      setFetchResult(data)
      // Refresh events list after a short delay (client-side only)
      setTimeout(() => {
        if (typeof window !== 'undefined') {
          window.location.reload()
        }
      }, 1500)
    } catch (error) {
      setFetchResult({ status: 'error', count: 0 })
    } finally {
      setIsFetching(false)
    }
  }

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const response = await fetch('/api/v1/events?limit=50')
        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}))
          throw new Error(errorData.details || `Failed to fetch: ${response.status}`)
        }
        const data = await response.json()
        const apiEvents: ConflictEvent[] = data.events.map((e: any) => ({
          id: e.id,
          title: e.title,
          latitude: e.latitude || 0,
          longitude: e.longitude || 0,
          severity: e.severity_score || 1,
          published_date: e.event_timestamp ? new Date(e.event_timestamp).toISOString().split('T')[0] : 'Unknown',
          country_code: e.country_code || undefined,
        }))
        setEvents(apiEvents)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error')
      } finally {
        setIsLoading(false)
      }
    }

    fetchEvents()
  }, [])

  const getSeverityBadge = (severity: number) => {
    const variants = {
      1: 'severity1',
      2: 'severity2',
      3: 'severity3',
      4: 'severity4',
      5: 'severity5',
    } as const
    const variant = variants[severity as keyof typeof variants] || 'default'
    const labels = {
      1: 'Low',
      2: 'Moderate',
      3: 'Elevated',
      4: 'High',
      5: 'Critical',
    }
    return <Badge variant={variant}>{labels[severity as keyof typeof labels] || `Level ${severity}`}</Badge>
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-background">
        <Card className="w-full max-w-md">
          <CardHeader>
            <Skeleton className="h-8 w-3/4" />
            <Skeleton className="h-4 w-1/2" />
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <Skeleton className="h-32 w-full" />
              <Skeleton className="h-32 w-full" />
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <main className="min-h-screen bg-background">
      {/* Header with shadcn Navigation Menu */}
      <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-16 items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="text-2xl">🌍</span>
            <h1 className="text-xl font-bold text-foreground">WarTracker</h1>
            <Badge variant="outline" className="ml-2">v1.0</Badge>
          </div>
          
          <div className="flex items-center gap-4">
            <Button 
              onClick={handleFetchData} 
              disabled={isFetching}
              variant="default"
              size="sm"
            >
              {isFetching && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
              {isFetching ? 'Fetching...' : '🔄 Pull Latest Data'}
            </Button>
            
            <NavigationMenu>
              <NavigationMenuList>
                <NavigationMenuItem>
                  <NavigationMenuLink
                    className={cn(
                      navigationMenuTriggerStyle(),
                      activeTab === 'map' && 'bg-accent'
                    )}
                    onClick={() => setActiveTab('map')}
                  >
                    🗺️ Map
                  </NavigationMenuLink>
                </NavigationMenuItem>
                <NavigationMenuItem>
                  <NavigationMenuLink
                    className={cn(
                      navigationMenuTriggerStyle(),
                      activeTab === 'timeline' && 'bg-accent'
                    )}
                    onClick={() => setActiveTab('timeline')}
                  >
                    📅 Timeline
                  </NavigationMenuLink>
                </NavigationMenuItem>
                <NavigationMenuItem>
                  <NavigationMenuLink
                    className={cn(
                      navigationMenuTriggerStyle(),
                      activeTab === 'alerts' && 'bg-accent'
                    )}
                    onClick={() => setActiveTab('alerts')}
                  >
                    🔔 Alerts
                  </NavigationMenuLink>
                </NavigationMenuItem>
              </NavigationMenuList>
            </NavigationMenu>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="container py-8">
        {fetchResult && (
          <Alert className="mb-6" variant={fetchResult.status === 'success' ? 'default' : 'destructive'}>
            <AlertDescription>
              {fetchResult.status === 'success' 
                ? `✅ Successfully collected ${fetchResult.count} new events!`
                : '❌ Failed to fetch data. Please try again.'}
            </AlertDescription>
          </Alert>
        )}
        
        {error ? (
          <Alert variant="destructive" className="mb-6">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        ) : (
          <>
            {/* Stats Overview */}
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4 mb-8">
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Total Events</CardTitle>
                  <span className="text-2xl">📊</span>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{events.length}</div>
                  <p className="text-xs text-muted-foreground">Last 30 days</p>
                </CardContent>
              </Card>
              
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Critical</CardTitle>
                  <span className="text-2xl">🔴</span>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{events.filter(e => e.severity >= 4).length}</div>
                  <p className="text-xs text-muted-foreground">Severity 4-5</p>
                </CardContent>
              </Card>
              
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Countries</CardTitle>
                  <span className="text-2xl">🌐</span>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{new Set(events.map(e => e.country_code)).size}</div>
                  <p className="text-xs text-muted-foreground">Affected regions</p>
                </CardContent>
              </Card>
              
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Last Update</CardTitle>
                  <span className="text-2xl">⏰</span>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{events.length > 0 ? 'Today' : 'N/A'}</div>
                  <p className="text-xs text-muted-foreground">Real-time data</p>
                </CardContent>
              </Card>
            </div>

            {/* Tab Content */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  {activeTab === 'map' && '🗺️ Global Conflict Map'}
                  {activeTab === 'timeline' && '📅 Event Timeline'}
                  {activeTab === 'alerts' && '🔔 Alerts & Notifications'}
                </CardTitle>
                <CardDescription>
                  {activeTab === 'map' && 'Real-time visualization of conflicts worldwide. Click markers for details.'}
                  {activeTab === 'timeline' && 'Chronological view of conflict events.'}
                  {activeTab === 'alerts' && 'Manage your alert preferences and notifications.'}
                </CardDescription>
              </CardHeader>
              <CardContent>
                {activeTab === 'map' && (
                  <div className="space-y-6">
                    <div className="flex gap-2 mb-4">
                      <Badge variant="severity1">Low</Badge>
                      <Badge variant="severity2">Moderate</Badge>
                      <Badge variant="severity3">Elevated</Badge>
                      <Badge variant="severity4">High</Badge>
                      <Badge variant="severity5">Critical</Badge>
                    </div>
                    <ConflictMap events={events} />
                  </div>
                )}
                
                {activeTab === 'timeline' && (
                  <Timeline events={events} />
                )}
                
                {activeTab === 'alerts' && (
                  <Alerts events={events} />
                )}
              </CardContent>
            </Card>
          </>
        )}
      </div>

      {/* Footer */}
      <footer className="border-t bg-muted/50 mt-8">
        <div className="container py-6">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-sm text-muted-foreground text-center md:text-left">
              © 2026 WarTracker. Data provided for informational purposes only.
            </p>
            <div className="flex gap-4">
              <Button variant="link" className="text-sm">Privacy Policy</Button>
              <Button variant="link" className="text-sm">Terms of Service</Button>
              <Button variant="link" className="text-sm">About</Button>
            </div>
          </div>
        </div>
      </footer>
    </main>
  )
}
