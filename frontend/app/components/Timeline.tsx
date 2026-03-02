'use client'

import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Separator } from '@/components/ui/separator'
import { ScrollArea } from '@/components/ui/scroll-area'
import { cn } from '@/lib/utils'

interface ConflictEvent {
  id: number
  title: string
  severity: number
  published_date: string
  country_code: string
}

interface TimelineProps {
  events: ConflictEvent[]
}

export function Timeline({ events }: TimelineProps) {
  const [selectedDate, setSelectedDate] = useState<string | null>(null)

  // Group events by date
  const eventsByDate = events.reduce((acc, event) => {
    const date = event.published_date
    if (!acc[date]) acc[date] = []
    acc[date].push(event)
    return acc
  }, {} as Record<string, ConflictEvent[]>)

  const sortedDates = Object.keys(eventsByDate).sort((a, b) => new Date(b).getTime() - new Date(a).getTime())

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

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          📅 Conflict Timeline
        </CardTitle>
        <CardDescription>
          Chronological view of conflict events
        </CardDescription>
      </CardHeader>
      <CardContent>
        {sortedDates.length === 0 ? (
          <p className="text-muted-foreground text-center py-8">No events to display</p>
        ) : (
          <ScrollArea className="h-[600px] pr-4">
            <div className="space-y-6">
              {sortedDates.map(date => {
                const dateEvents = eventsByDate[date]
                const isSelected = selectedDate === date
                
                return (
                  <div key={date} className="relative pl-6">
                    {/* Timeline line */}
                    <div className="absolute left-0 top-0 bottom-0 w-0.5 bg-border" />
                    <div className="absolute left-[-4px] top-4 w-2 h-2 rounded-full bg-primary" />
                    
                    <Button
                      variant="ghost"
                      onClick={() => setSelectedDate(isSelected ? null : date)}
                      className="w-full justify-between p-0 h-auto hover:bg-transparent"
                    >
                      <div className="text-left">
                        <h3 className="text-lg font-semibold text-foreground">
                          {new Date(date).toLocaleDateString('en-US', { 
                            weekday: 'long', 
                            year: 'numeric', 
                            month: 'long', 
                            day: 'numeric' 
                          })}
                        </h3>
                      </div>
                      <Badge variant="secondary">
                        {dateEvents.length} events
                      </Badge>
                    </Button>
                    
                    {isSelected && (
                      <div className="mt-4 space-y-3 animate-in fade-in slide-in-from-top-2 duration-200">
                        {dateEvents.map(event => (
                          <Card
                            key={event.id}
                            className={cn(
                              "border-l-4",
                              event.severity >= 4 && "border-l-red-500 bg-red-50 dark:bg-red-900/20",
                              event.severity === 3 && "border-l-orange-500 bg-orange-50 dark:bg-orange-900/20",
                              event.severity <= 2 && "border-l-green-500 bg-green-50 dark:bg-green-900/20"
                            )}
                          >
                            <CardContent className="p-4">
                              <div className="flex justify-between items-start">
                                <div className="flex-1">
                                  <h4 className="font-semibold text-foreground mb-1">
                                    {event.title}
                                  </h4>
                                  <p className="text-sm text-muted-foreground">
                                    {event.country_code && `📍 ${event.country_code}`}
                                  </p>
                                </div>
                                <Badge variant={getSeverityBadge(event.severity)}>
                                  S{event.severity}
                                </Badge>
                              </div>
                            </CardContent>
                          </Card>
                        ))}
                      </div>
                    )}
                    
                    <Separator className="my-4" />
                  </div>
                )
              })}
            </div>
          </ScrollArea>
        )}
      </CardContent>
    </Card>
  )
}
