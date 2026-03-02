import { NextResponse } from 'next/server'

export async function GET(request: Request) {
  try {
    // Get search params from the request
    const { searchParams } = new URL(request.url)
    const limit = searchParams.get('limit') || '50'
    
    // Fetch from backend service
    const backendUrl = `http://backend:8000/api/v1/events?limit=${limit}`
    const response = await fetch(backendUrl)
    
    if (!response.ok) {
      throw new Error(`Backend returned ${response.status}`)
    }
    
    const data = await response.json()
    
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error fetching from backend:', error)
    return NextResponse.json(
      { error: 'Failed to fetch events', details: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    )
  }
}
