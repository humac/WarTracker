"""Collector Manager - Orchestrates all data collectors

Manages all data collectors and orchestrates data collection.
Prioritizes free sources (GDELT) by default.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from .base import BaseCollector
from .gdelt import GDELTCollector


class CollectorManager:
    """
    Manages all data collectors and orchestrates data collection.
    
    Prioritizes free sources (GDELT) by default.
    """
    
    def __init__(self):
        """Initialize collector manager with available collectors"""
        # Primary collector (FREE - no API key needed)
        self.collectors: Dict[str, BaseCollector] = {
            "gdelt": GDELTCollector(max_records=100)
        }
        
        # Optional collectors (require API keys - not enabled by default)
        # Uncomment and configure API keys to enable:
        # from .acled import ACLEDCollector
        # from .newsapi import NewsAPICollector
        # self.collectors["acled"] = ACLEDCollector()
        # self.collectors["newsapi"] = NewsAPICollector()
        
        # Collection statistics
        self.stats = {
            "total_collected": 0,
            "by_source": {},
            "last_collection": None,
            "errors": []
        }
    
    async def collect_all(self, sources: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Run all enabled collectors and aggregate results.
        
        Args:
            sources: Optional list of source names to collect from.
                    If None, collects from all enabled sources.
        
        Returns:
            List of normalized event dictionaries
        """
        if sources is None:
            sources = list(self.collectors.keys())
        
        all_events = []
        
        print(f"Starting collection from {len(sources)} sources: {sources}")
        
        for source_name in sources:
            if source_name not in self.collectors:
                print(f"Warning: Unknown source '{source_name}', skipping")
                continue
            
            collector = self.collectors[source_name]
            
            # Skip if API key required but not configured
            if collector.requires_api_key and not self._has_api_key(source_name):
                print(f"Skipping {source_name}: API key not configured")
                continue
            
            print(f"Collecting from {source_name}...")
            
            try:
                events = await collector.collect()
                
                # Filter out invalid events
                valid_events = [
                    e for e in events 
                    if collector.validate_event(e)
                ]
                
                all_events.extend(valid_events)
                
                # Update stats
                self.stats["by_source"][source_name] = len(valid_events)
                self.stats["total_collected"] += len(valid_events)
                
                print(f"Collected {len(valid_events)} valid events from {source_name}")
                
                # Update source status in database (if connected)
                await self._update_source_status(source_name, "success", len(valid_events))
                
            except Exception as e:
                error_msg = f"Error collecting from {source_name}: {str(e)}"
                print(error_msg)
                self.stats["errors"].append({
                    "source": source_name,
                    "error": str(e),
                    "timestamp": datetime.now(timezone.utc)
                })
                await self._update_source_status(source_name, "error", 0, str(e))
        
        self.stats["last_collection"] = datetime.now(timezone.utc)
        
        print(f"Collection complete: {len(all_events)} total events")
        
        return all_events
    
    def _has_api_key(self, source_name: str) -> bool:
        """
        Check if API key is configured for a source.
        
        Args:
            source_name: Name of the data source
            
        Returns:
            True if API key is configured, False otherwise
        """
        # Import settings here to avoid circular imports
        try:
            from app.config import settings
            
            if source_name == "acled":
                return bool(getattr(settings, "acled_api_key", None))
            elif source_name == "newsapi":
                return bool(getattr(settings, "newsapi_key", None))
            else:
                # GDELT doesn't need API key
                return True
        except Exception:
            return False
    
    async def _update_source_status(
        self, 
        source_id: str, 
        status: str, 
        events_collected: int,
        error: Optional[str] = None
    ):
        """
        Update source status in database.
        
        Args:
            source_id: Source identifier
            status: Status string (success/error)
            events_collected: Number of events collected
            error: Error message if status is error
        """
        # This would update the 'sources' table in the database
        # For now, just log it
        print(f"Source {source_id}: {status} ({events_collected} events)")
    
    def get_available_sources(self) -> List[Dict[str, Any]]:
        """
        Get list of available data sources.
        
        Returns:
            List of source dictionaries with metadata
        """
        sources = []
        
        for name, collector in self.collectors.items():
            sources.append({
                "id": name,
                "name": collector.name,
                "description": collector.description,
                "requires_api_key": collector.requires_api_key,
                "api_key_configured": self._has_api_key(name) if collector.requires_api_key else True,
                "enabled": True
            })
        
        return sources
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get collection statistics.
        
        Returns:
            Dictionary with collection stats
        """
        return {
            **self.stats,
            "available_sources": list(self.collectors.keys()),
            "enabled_sources": [
                name for name, collector in self.collectors.items()
                if not collector.requires_api_key or self._has_api_key(name)
            ]
        }
