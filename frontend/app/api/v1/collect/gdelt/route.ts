import { NextResponse } from 'next/server'

export async function POST() {
  try {
    // Forward POST request to backend collector
    const backendUrl = 'http://backend:8000/api/v1/collect/gdelt'
    const response = await fetch(backendUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    })
    
    const data = await response.json()
    
    // Always return 200 with the backend's response (even if it's an error status)
    return NextResponse.json(data, { status: 200 })
  } catch (error) {
    console.error('Error calling backend collector:', error)
    return NextResponse.json(
      { 
        status: 'error', 
        message: 'Failed to connect to collector service',
        count: 0 
      },
      { status: 200 }
    )
  }
}
