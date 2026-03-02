"""Test GDELT and base collectors."""
import pytest
from datetime import datetime, timezone
from app.collectors.gdelt import GDELTCollector
from app.collectors.base import BaseCollector


class TestGDELTCollector:
    """Test suite for GDELT collector."""
    
    @pytest.fixture
    def collector(self):
        """Create a GDELT collector instance."""
        return GDELTCollector(max_records=10)
    
    def test_collector_initialization(self, collector):
        """Test collector initializes with correct attributes."""
        assert collector.name == "gdelt"
        assert collector.requires_api_key is False
        assert collector.max_records == 10
        assert "GDELT" in collector.description
    
    def test_classify_event_type_battle(self, collector):
        """Test event type classification for battle-related keywords."""
        assert collector._classify_event_type("Battle erupts in eastern region") == "battle"
        assert collector._classify_event_type("Combat forces engage rebels") == "battle"
        assert collector._classify_event_type("Fighting breaks out at border") == "battle"
        assert collector._classify_event_type("Military clash reported") == "battle"
    
    def test_classify_event_type_protest(self, collector):
        """Test event type classification for protest-related keywords."""
        assert collector._classify_event_type("Protest in capital city") == "protest"
        assert collector._classify_event_type("Demonstration turns violent") == "protest"
        assert collector._classify_event_type("Rally against government") == "protest"
    
    def test_classify_event_type_riot(self, collector):
        """Test event type classification for riot-related keywords."""
        assert collector._classify_event_type("Riot breaks out in streets") == "riot"
        assert collector._classify_event_type("Civil unrest continues") == "riot"
        assert collector._classify_event_type("Violence erupts in city") == "riot"
    
    def test_classify_event_type_attack(self, collector):
        """Test event type classification for attack-related keywords."""
        assert collector._classify_event_type("Bomb explosion in market") == "attack"
        assert collector._classify_event_type("Terrorist attack claimed") == "attack"
        assert collector._classify_event_type("Airstrike hits facility") == "attack"
    
    def test_classify_event_type_military(self, collector):
        """Test event type classification for military-related keywords."""
        assert collector._classify_event_type("Military deployment announced") == "military_action"
        assert collector._classify_event_type("Army troops mobilize") == "military_action"
        assert collector._classify_event_type("Soldiers cross border") == "military_action"
    
    def test_classify_event_type_conflict(self, collector):
        """Test event type classification for conflict-related keywords."""
        assert collector._classify_event_type("Conflict escalates in region") == "conflict"
        assert collector._classify_event_type("War tensions rise") == "conflict"
        assert collector._classify_event_type("Crisis deepens") == "conflict"
    
    def test_classify_event_type_other(self, collector):
        """Test event type classification defaults to 'other'."""
        assert collector._classify_event_type("Economic report released") == "other"
        assert collector._classify_event_type("Political meeting held") == "other"
    
    def test_estimate_severity(self, collector):
        """Test severity estimation based on event type."""
        assert collector._estimate_severity("battle") == 5
        assert collector._estimate_severity("attack") == 5
        assert collector._estimate_severity("riot") == 4
        assert collector._estimate_severity("military_action") == 4
        assert collector._estimate_severity("conflict") == 3
        assert collector._estimate_severity("protest") == 2
        assert collector._estimate_severity("other") == 2
    
    def test_get_country_centroid_ukraine(self, collector):
        """Test country centroid lookup for Ukraine."""
        lat, lon = collector._get_country_centroid("ukraine")
        assert lat == 48.3794
        assert lon == 31.1656
    
    def test_get_country_centroid_russia(self, collector):
        """Test country centroid lookup for Russia."""
        lat, lon = collector._get_country_centroid("russia")
        assert lat == 61.5240
        assert lon == 105.3188
    
    def test_get_country_centroid_default(self, collector):
        """Test country centroid returns default for unknown country."""
        lat, lon = collector._get_country_centroid("unknown_country")
        assert lat == 0.0
        assert lon == 0.0
    
    def test_normalize_article_basic(self, collector):
        """Test article normalization with basic fields."""
        article = {
            "title": "Test Event Report",
            "snippet": "Test description",
            "seendate": "20260302T120000",
            "sourcecountry": "Ukraine",
            "url": "https://example.com/article"
        }
        
        event = collector.normalize(article)
        
        assert event["title"] == "Test Event Report"
        assert event["description"] == "Test description"
        assert event["event_type"] == "other"
        assert event["severity_score"] == 2
        assert event["country_code"] == "UK"
        assert event["region_name"] == "Ukraine"
        assert event["verification_status"] == "unverified"
        assert event["confidence_score"] == 0.5
        assert event["is_active"] is True
        assert "POINT(" in event["location"]
        assert event["conflict_id"].startswith("gdelt_")
    
    def test_normalize_article_date_parsing_full(self, collector):
        """Test date parsing with full timestamp."""
        article = {
            "title": "Test",
            "seendate": "20260302T143000",
            "sourcecountry": "Ukraine"
        }
        
        event = collector.normalize(article)
        
        assert event["event_timestamp"].year == 2026
        assert event["event_timestamp"].month == 3
        assert event["event_timestamp"].day == 2
        assert event["event_timestamp"].hour == 14
        assert event["event_timestamp"].minute == 30
    
    def test_normalize_article_date_parsing_short(self, collector):
        """Test date parsing with date only."""
        article = {
            "title": "Test",
            "seendate": "20260302",
            "sourcecountry": "Ukraine"
        }
        
        event = collector.normalize(article)
        
        assert event["event_timestamp"].year == 2026
        assert event["event_timestamp"].month == 3
        assert event["event_timestamp"].day == 2
    
    def test_normalize_article_invalid_date(self, collector):
        """Test date parsing falls back to UTC now on invalid date."""
        article = {
            "title": "Test",
            "seendate": "invalid_date",
            "sourcecountry": "Ukraine"
        }
        
        event = collector.normalize(article)
        
        # Should default to current UTC time
        assert event["event_timestamp"] is not None
    
    def test_normalize_article_location_wkt(self, collector):
        """Test location is in WKT format."""
        article = {
            "title": "Test",
            "seendate": "20260302",
            "sourcecountry": "Ukraine"
        }
        
        event = collector.normalize(article)
        
        assert event["location"].startswith("POINT(")
        assert event["location"].endswith(")")
    
    def test_normalize_article_conflict_classification(self, collector):
        """Test event classification based on title keywords."""
        article = {
            "title": "Battle erupts in eastern Ukraine",
            "seendate": "20260302",
            "sourcecountry": "Ukraine"
        }
        
        event = collector.normalize(article)
        
        assert event["event_type"] == "battle"
        assert event["severity_score"] == 5


class TestBaseCollector:
    """Test suite for base collector class."""
    
    @pytest.fixture
    def concrete_collector(self):
        """Create a concrete implementation of BaseCollector for testing."""
        class TestCollector(BaseCollector):
            name = "test"
            description = "Test collector"
            
            async def fetch(self):
                return [{"title": "Test"}]
            
            def normalize(self, raw_data):
                return {
                    "title": raw_data["title"],
                    "event_timestamp": datetime.now(timezone.utc),
                    "location": "POINT(0 0)"
                }
        
        return TestCollector()
    
    def test_base_collector_is_abstract(self):
        """Test that BaseCollector cannot be instantiated directly."""
        with pytest.raises(TypeError):
            BaseCollector()
    
    def test_concrete_collector_attributes(self, concrete_collector):
        """Test concrete collector has required attributes."""
        assert concrete_collector.name == "test"
        assert concrete_collector.description == "Test collector"
    
    def test_collect_method_sync(self, concrete_collector):
        """Test the main collect method (synchronous wrapper)."""
        # Note: collect() is async, tested via integration tests
        # This validates the method exists and returns correct type
        import asyncio
        events = asyncio.run(concrete_collector.collect())
        
        assert len(events) == 1
        assert events[0]["title"] == "Test"
    
    def test_validate_event_valid(self, concrete_collector):
        """Test validation of valid event."""
        event = {
            "title": "Test Event",
            "event_timestamp": datetime.now(timezone.utc),
            "location": "POINT(30.5 50.5)"
        }
        
        assert concrete_collector.validate_event(event) is True
    
    def test_validate_event_missing_title(self, concrete_collector):
        """Test validation fails without title."""
        event = {
            "event_timestamp": datetime.now(timezone.utc),
            "location": "POINT(30.5 50.5)"
        }
        
        assert concrete_collector.validate_event(event) is False
    
    def test_validate_event_missing_timestamp(self, concrete_collector):
        """Test validation fails without timestamp."""
        event = {
            "title": "Test Event",
            "location": "POINT(30.5 50.5)"
        }
        
        assert concrete_collector.validate_event(event) is False
    
    def test_validate_event_missing_location(self, concrete_collector):
        """Test validation fails without location."""
        event = {
            "title": "Test Event",
            "event_timestamp": datetime.now(timezone.utc)
        }
        
        assert concrete_collector.validate_event(event) is False
    
    def test_validate_event_invalid_location_format(self, concrete_collector):
        """Test validation fails with invalid location format."""
        event = {
            "title": "Test Event",
            "event_timestamp": datetime.now(timezone.utc),
            "location": "INVALID_LOCATION"
        }
        
        assert concrete_collector.validate_event(event) is False
    
    def test_validate_event_none_location(self, concrete_collector):
        """Test validation fails with None location."""
        event = {
            "title": "Test Event",
            "event_timestamp": datetime.now(timezone.utc),
            "location": None
        }
        
        assert concrete_collector.validate_event(event) is False
