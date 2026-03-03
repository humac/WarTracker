"""GDELT Project Collector - FREE, no API key required

GDELT (Global Database of Events, Language, and Tone) monitors the world's 
broadcast, print, and web news from nearly every country in over 100 languages.

Supported by Google Jigsaw.
Docs: https://www.gdeltproject.org/data.html
"""
import httpx
import asyncio
from typing import List, Dict, Any
from datetime import datetime, timedelta, timezone

from .base import BaseCollector


class GDELTCollector(BaseCollector):
    """
    GDELT (Global Database of Events, Language, and Tone) Collector
    
    GDELT monitors the world's broadcast, print, and web news from nearly 
    every country in over 100 languages. Completely FREE and open.
    
    Supported by Google Jigsaw.
    
    Features:
    - No API key required
    - Global coverage
    - Real-time updates
    - Event types: conflicts, protests, riots, battles, etc.
    
    Docs: https://www.gdeltproject.org/data.html
    """
    
    name = "gdelt"
    description = "GDELT Project - Global event database (free)"
    requires_api_key = False
    
    # GDELT 2.0 API endpoints
    BASE_URL = "https://api.gdeltproject.org/api/v2/doc/doc"
    
    # Search queries for conflict-related events (more specific for better results)
    CONFLICT_QUERIES = [
        "war",
        "bombing",
        "airstrike",
        "missile attack",
        "military offensive",
        "armed conflict",
        "ceasefire violation",
        "shelling",
        "artillery fire",
        "insurgent attack"
    ]
    
    def __init__(self, max_records: int = 250, timeout: float = 60.0):
        """
        Initialize GDELT collector.
        
        Args:
            max_records: Maximum number of records to fetch per query
            timeout: Request timeout in seconds (default: 60.0)
        """
        self.max_records = max_records
        self.timeout = timeout  # Store timeout
    
    async def fetch(self) -> List[Dict[str, Any]]:
        """
        Fetch conflict-related events from GDELT.
        
        Returns:
            List of raw article/event dictionaries
        """
        all_articles = []
        
        # GDELT requires a User-Agent header
        headers = {
            "User-Agent": "WarTracker/1.0 (Conflict Tracking Platform)"
        }
        
        # Use configured timeout
        async with httpx.AsyncClient(
            headers=headers,
            timeout=httpx.Timeout(self.timeout, connect=15.0, read=45.0)
        ) as client:
            # Fetch recent conflict news (last 24 hours)
            # GDELT requires parentheses around OR'd terms
            query = "(" + " OR ".join(self.CONFLICT_QUERIES) + ")"
            
            params = {
                "query": query,
                "format": "json",
                "maxrecords": str(self.max_records),
                "sort": "Date",
                "lang": "english"
            }
            
            try:
                # Retry up to 3 times on connection errors
                for attempt in range(3):
                    try:
                        response = await client.get(self.BASE_URL, params=params)
                        break
                    except httpx.ConnectTimeout:
                        if attempt < 2:
                            print(f"GDELT connection timeout, retrying ({attempt+1}/3)...")
                            await asyncio.sleep(2)
                        else:
                            raise
                
                print(f"GDELT Response status: {response.status_code}")
                print(f"GDELT Response length: {len(response.content)} bytes")
                if len(response.content) < 500:
                    print(f"GDELT Response preview: {response.text[:200]}")
                
                response.raise_for_status()
                
                # GDELT returns JSON with 'articles' array
                data = response.json()
                
                if isinstance(data, dict):
                    articles = data.get("articles", [])
                elif isinstance(data, list):
                    articles = data
                else:
                    articles = []
                
                all_articles.extend(articles)
                print(f"GDELT: Fetched {len(articles)} articles")
                if articles:
                    print(f"Sample article keys: {list(articles[0].keys())[:10]}")
                
            except httpx.HTTPStatusError as e:
                print(f"GDELT HTTP error {e.response.status_code}: {e}")
                print(f"Response: {e.response.text[:200]}")
                if e.response.status_code == 429:
                    print("Rate limited - waiting before retry...")
                    await asyncio.sleep(5)
            except httpx.HTTPError as e:
                print(f"GDELT HTTP error: {type(e).__name__}: {e}")
            except Exception as e:
                print(f"GDELT error: {type(e).__name__}: {e}")
                import traceback
                traceback.print_exc()
        
        return all_articles
    
    def normalize(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize GDELT article to WarTracker event schema.
        
        Note: GDELT v2/doc API doesn't provide lat/lon directly.
        We use source country for rough geolocation.
        
        Args:
            article: Raw GDELT article dictionary
            
        Returns:
            Normalized event dictionary
        """
        # GDELT v2/doc doesn't provide lat/lon - use country centroids as approximation
        # This is a limitation - for production, use GDELT GKG or event API
        country = article.get("sourcecountry", "").lower()
        latitude, longitude = self._get_country_centroid(country)
        
        # Parse date (GDELT uses YYYYMMDDTHHMMSS format)
        date_str = article.get("seendate", "")
        try:
            if len(date_str) >= 14:
                event_date = datetime.strptime(date_str[:14], "%Y%m%dT%H%M%S")
            elif len(date_str) >= 8:
                event_date = datetime.strptime(date_str[:8], "%Y%m%d")
            else:
                event_date = datetime.now(timezone.utc)
        except (ValueError, TypeError):
            event_date = datetime.now(timezone.utc)
        
        # Determine event type from keywords in title
        title = article.get("title", "").lower()
        event_type = self._classify_event_type(title)
        
        # Estimate severity based on event type
        severity = self._estimate_severity(event_type)
        
        return {
            "title": article.get("title", "Untitled Event"),
            "description": article.get("snippet", ""),
            "event_timestamp": event_date,
            "latitude": latitude,
            "longitude": longitude,
            "severity_score": severity,
            "event_type": event_type,
            "actors_involved": [],
            "country_code": article.get("sourcecountry", "")[:2].upper() if article.get("sourcecountry") else None,
            "region_name": article.get("sourcecountry", ""),
            "verification_status": "unverified",
            "confidence_score": 0.5,  # Single source
            "is_active": True,
            "ai_summary": None,
            "conflict_id": f"gdelt_{hash(article.get('url', '')) % 1000000}"
        }
    
    def _classify_event_type(self, title: str) -> str:
        """
        Classify event type based on title keywords.
        
        Args:
            title: Article title
            
        Returns:
            Event type string
        """
        title_lower = title.lower()
        
        if any(word in title_lower for word in ["battle", "combat", "fighting", "clash"]):
            return "battle"
        elif any(word in title_lower for word in ["protest", "demonstration", "rally"]):
            return "protest"
        elif any(word in title_lower for word in ["riot", "unrest", "violence"]):
            return "riot"
        elif any(word in title_lower for word in ["bomb", "explosion", "attack", "strike"]):
            return "attack"
        elif any(word in title_lower for word in ["military", "army", "troops", "soldiers"]):
            return "military_action"
        elif any(word in title_lower for word in ["crisis", "conflict", "war"]):
            return "conflict"
        else:
            return "other"
    
    def _estimate_severity(self, event_type: str) -> int:
        """
        Estimate severity score (1-5) based on event type.
        
        Args:
            event_type: Classified event type
            
        Returns:
            Severity score 1-5
        """
        severity_map = {
            "battle": 5,
            "attack": 5,
            "riot": 4,
            "military_action": 4,
            "conflict": 3,
            "protest": 2,
            "other": 2
        }
        return severity_map.get(event_type, 2)
    
    def _get_country_centroid(self, country: str) -> tuple:
        """
        Get approximate lat/lon centroid for a country.
        
        Args:
            country: Country name
            
        Returns:
            Tuple of (latitude, longitude)
        """
        # Approximate centroids for common countries
        centroids = {
            "ukraine": (48.3794, 31.1656),
            "russia": (61.5240, 105.3188),
            "israel": (31.0461, 34.8516),
            "palestinian territories": (31.9522, 35.2332),
            "syria": (34.8021, 38.9968),
            "iran": (32.4279, 53.6880),
            "iraq": (33.2232, 43.6793),
            "yemen": (15.5527, 48.5164),
            "afghanistan": (33.9391, 67.7100),
            "pakistan": (30.3753, 69.3451),
            "india": (20.5937, 78.9629),
            "china": (35.8617, 104.1954),
            "north korea": (40.3399, 127.5101),
            "south korea": (35.9078, 127.7669),
            "japan": (36.2048, 138.2529),
            "united states": (37.0902, -95.7129),
            "mexico": (23.6345, -102.5528),
            "brazil": (-14.2350, -51.9253),
            "argentina": (-38.4161, -63.6167),
            "serbia": (44.0165, 21.0059),
            "albania": (41.1533, 20.1683),
            "indonesia": (-0.7893, 113.9213),
            "philippines": (12.8797, 121.7740),
            "thailand": (15.8700, 100.9925),
            "vietnam": (14.0583, 108.2772),
            "myanmar": (21.9162, 95.9560),
            "nigeria": (9.0820, 8.6753),
            "kenya": (-0.0236, 37.9062),
            "ethiopia": (9.1450, 40.4897),
            "somalia": (5.1521, 46.1996),
            "sudan": (12.8628, 30.2176),
            "libya": (26.3351, 17.2283),
            "egypt": (26.8206, 30.8025),
            "turkey": (38.9637, 35.2433),
            "france": (46.2276, 2.2137),
            "germany": (51.1657, 10.4515),
            "united kingdom": (55.3781, -3.4360),
            "spain": (40.4637, -3.7492),
            "italy": (41.8719, 12.5674),
            "poland": (51.9194, 19.1451),
            "default": (0.0, 0.0)  # Unknown location
        }
        
        return centroids.get(country, centroids["default"])
