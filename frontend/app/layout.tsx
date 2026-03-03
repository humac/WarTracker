import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import 'leaflet/dist/leaflet.css'
import 'leaflet.markercluster/dist/MarkerCluster.css'
import 'leaflet.markercluster/dist/MarkerCluster.Default.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'WarTracker - Real-time Global Conflict Tracking',
  description: 'Real-time, verified information on global conflicts by continuously monitoring multiple data sources',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  )
}
