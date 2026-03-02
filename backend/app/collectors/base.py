"""Base collector class for all data sources"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from datetime import datetime


class BaseCollector(ABC):
    """Abstract base class for all data collectors"""
    
    # Collector metadata
    name: str = "base"
    description: str = "Base collector"
    requires_api_key: bool = False
    
    @abstractmethod
    async def fetch(self) -> List[Dict[str, Any]]:
        """
        Fetch raw data from source.
        
        Returns:
            List of raw event dictionaries
        """
        pass
    
    @abstractmethod
    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize raw data to unified schema.
        
        Args:
            raw_data: Raw event data from source
            
        Returns:
            Normalized event dictionary matching ConflictEvent schema
        """
        pass
    
    async def collect(self) -> List[Dict[str, Any]]:
        """
        Main collection method - fetches and normalizes data.
        
        Returns:
            List of normalized event dictionaries
        """
        try:
            raw_data = await self.fetch()
            return [self.normalize(item) for item in raw_data]
        except Exception as e:
            print(f"Error in {self.name} collector: {e}")
            return []
    
    def validate_event(self, event: Dict[str, Any]) -> bool:
        """
        Validate normalized event has required fields.
        
        Args:
            event: Normalized event dictionary
            
        Returns:
            True if valid, False otherwise
        """
        required_fields = ['title', 'event_timestamp', 'latitude', 'longitude']
        return all(field in event and event[field] is not None for field in required_fields)
