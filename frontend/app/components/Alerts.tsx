'use client'

import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Button } from '@/components/ui/button'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { ScrollArea } from '@/components/ui/scroll-area'
import { cn } from '@/lib/utils'

interface ConflictEvent {
  id: number
  title: string
  severity: number
  published_date: string
  country_code: string
}

interface AlertsProps {
  events: ConflictEvent[]
}

export function Alerts({ events }: AlertsProps) {
  const [filter, setFilter] = useState<'all' | 'high' | 'medium' | 'low'>('all')
  const [sortBy, setSortBy] = useState<'date' | 'severity'>('severity')
  const [selectedEvent, setSelectedEvent] = useState<ConflictEvent | null>(null)

  // Filter events by severity
  const filteredEvents = events.filter(event => {
    if (filter === 'high') return event.severity >= 4
    if (filter === 'medium') return event.severity === 3
    if (filter === 'low') return event.severity <= 2
    return true
  })

  // Sort events
  const sortedEvents = [...filteredEvents].sort((a, b) => {
    if (sortBy === 'severity') return b.severity - a.severity
    return new Date(b.published_date).getTime() - new Date(a.published_date).getTime()
  })

  const highSeverityCount = events.filter(e => e.severity >= 4).length
  const mediumSeverityCount = events.filter(e => e.severity === 3).length
  const lowSeverityCount = events.filter(e => e.severity <= 2).length

  const getSeverityBadge = (severity: number) => {
    const variants = {
      1: 'severity1',
      2: 'severity2',
      3: 'severity3',
      4: 'severity4',
      5: 'severity5',
    } as const
    const variant = variants[severity as keyof typeof variants] || 'default'
    return variant
  }

  const getAlertVariant = (severity: number) => {
    if (severity >= 4) return 'destructive'
    if (severity === 3) return 'warning' as any
    return 'default'
  }

  const getSeverityLabel = (severity: number) => {
    const labels = {
      1: 'Low',
      2: 'Moderate',
      3: 'Elevated',
      4: 'High',
      5: 'Critical',
    }
    return labels[severity as keyof typeof labels] || `Level ${severity}`
  }

  return (
    <div className="space-y-6">
      {/* Summary Cards */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card className="border-red-200 dark:border-red-800">
          <CardHeader className="pb-2">
            <CardTitle className="text-3xl font-bold text-red-600 dark:text-red-400">
              {highSeverityCount}
            </CardTitle>
            <CardDescription>High Severity (4-5)</CardDescription>
          </CardHeader>
        </Card>
        <Card className="border-orange-200 dark:border-orange-800">
          <CardHeader className="pb-2">
            <CardTitle className="text-3xl font-bold text-orange-600 dark:text-orange-400">
              {mediumSeverityCount}
            </CardTitle>
            <CardDescription>Medium (3)</CardDescription>
          </CardHeader>
        </Card>
        <Card className="border-green-200 dark:border-green-800">
          <CardHeader className="pb-2">
            <CardTitle className="text-3xl font-bold text-green-600 dark:text-green-400">
              {lowSeverityCount}
            </CardTitle>
            <CardDescription>Low (1-2)</CardDescription>
          </CardHeader>
        </Card>
      </div>

      {/* Main Alerts Card */}
      <Card>
        <CardHeader>
          <CardTitle>🔔 Conflict Alerts</CardTitle>
          <CardDescription>
            Manage and monitor conflict alerts by severity
          </CardDescription>
        </CardHeader>
        <CardContent>
          {/* Filters */}
          <div className="flex flex-wrap gap-4 mb-6">
            <div className="flex items-center gap-2">
              <span className="text-sm font-medium">Filter:</span>
              <Select value={filter} onValueChange={(v) => setFilter(v as typeof filter)}>
                <SelectTrigger className="w-[180px]">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Severities</SelectItem>
                  <SelectItem value="high">High (4-5)</SelectItem>
                  <SelectItem value="medium">Medium (3)</SelectItem>
                  <SelectItem value="low">Low (1-2)</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="flex items-center gap-2">
              <span className="text-sm font-medium">Sort:</span>
              <Select value={sortBy} onValueChange={(v) => setSortBy(v as typeof sortBy)}>
                <SelectTrigger className="w-[150px]">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="severity">By Severity</SelectItem>
                  <SelectItem value="date">By Date</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          {/* Alerts List */}
          <ScrollArea className="h-[500px] pr-4">
            <div className="space-y-4">
              {sortedEvents.length === 0 ? (
                <p className="text-muted-foreground text-center py-8">No alerts match your filters</p>
              ) : (
                sortedEvents.map((event, index) => (
                  <Alert
                    key={event.id}
                    variant={getAlertVariant(event.severity)}
                    className={cn(
                      "border-l-4 transition-all hover:shadow-md",
                      event.severity >= 4 && "border-l-red-500 bg-red-50 dark:bg-red-900/20",
                      event.severity === 3 && "border-l-orange-500 bg-orange-50 dark:bg-orange-900/20",
                      event.severity <= 2 && "border-l-green-500 bg-green-50 dark:bg-green-900/20"
                    )}
                    style={{ animationDelay: `${index * 50}ms` }}
                  >
                    <AlertTitle className="flex items-center gap-2">
                      <Badge variant={getSeverityBadge(event.severity)}>
                        {getSeverityLabel(event.severity)}
                      </Badge>
                      {event.country_code && (
                        <span className="text-sm text-muted-foreground">
                          📍 {event.country_code}
                        </span>
                      )}
                      <span className="text-xs text-muted-foreground ml-auto">
                        {new Date(event.published_date).toLocaleDateString()}
                      </span>
                    </AlertTitle>
                    <AlertDescription className="mt-2">
                      <div className="flex justify-between items-start">
                        <p className="font-medium">{event.title}</p>
                        <Dialog>
                          <DialogTrigger asChild>
                            <Button variant="link" className="text-sm" onClick={() => setSelectedEvent(event)}>
                              Details →
                            </Button>
                          </DialogTrigger>
                          <DialogContent>
                            <DialogHeader>
                              <DialogTitle className="flex items-center gap-2">
                                <Badge variant={getSeverityBadge(event.severity)}>
                                  {getSeverityLabel(event.severity)}
                                </Badge>
                                Event Details
                              </DialogTitle>
                              <DialogDescription>
                                {new Date(event.published_date).toLocaleDateString()}
                              </DialogDescription>
                            </DialogHeader>
                            <div className="space-y-4">
                              <div>
                                <h4 className="font-semibold mb-2">Title</h4>
                                <p>{event.title}</p>
                              </div>
                              <div className="grid grid-cols-2 gap-4">
                                <div>
                                  <h4 className="font-semibold mb-2">Location</h4>
                                  <p>{event.country_code || 'Unknown'}</p>
                                </div>
                                <div>
                                  <h4 className="font-semibold mb-2">Severity</h4>
                                  <Badge variant={getSeverityBadge(event.severity)}>
                                    {getSeverityLabel(event.severity)}
                                  </Badge>
                                </div>
                              </div>
                            </div>
                            <DialogFooter>
                              <Button onClick={() => setSelectedEvent(null)}>Close</Button>
                            </DialogFooter>
                          </DialogContent>
                        </Dialog>
                      </div>
                    </AlertDescription>
                  </Alert>
                ))
              )}
            </div>
          </ScrollArea>

          <p className="mt-6 text-sm text-muted-foreground text-center">
            Showing {sortedEvents.length} of {events.length} alerts
          </p>
        </CardContent>
      </Card>
    </div>
  )
}
