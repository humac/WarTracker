from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from app.collectors.gdelt import GDELTCollector
from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime, timezone
import httpx
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


async def save_events_to_db(events: list, db: Session):
    """
    Save collected events to database in background.
    Reuses existing event creation logic.
    """
    for event in events:
        # Check if event already exists (by conflict_id)
        existing = db.execute(
            text("SELECT id FROM conflict_events WHERE conflict_id = :conflict_id"),
            {"conflict_id": event.get("conflict_id")}
        ).fetchone()
        
        if existing:
            continue  # Skip duplicates
        
        latitude = event.get("latitude", 0.0)
        longitude = event.get("longitude", 0.0)

        # Insert event using float lat/lon columns
        db.execute(
            text("""
                INSERT INTO conflict_events (
                    title, description, event_timestamp, latitude, longitude,
                    severity_score, event_type, country_code, region_name,
                    verification_status, confidence_score, is_active,
                    conflict_id
                ) VALUES (
                    :title, :description, :event_timestamp, :latitude, :longitude,
                    :severity_score, :event_type, :country_code, :region_name,
                    :verification_status, :confidence_score, :is_active,
                    :conflict_id
                )
            """),
            {
                "title": event.get("title", "Untitled Event"),
                "description": event.get("description", ""),
                "event_timestamp": event.get("event_timestamp", datetime.now(timezone.utc)),
                "latitude": latitude,
                "longitude": longitude,
                "severity_score": event.get("severity_score", 2),
                "event_type": event.get("event_type", "other"),
                "country_code": event.get("country_code"),
                "region_name": event.get("region_name"),
                "verification_status": event.get("verification_status", "unverified"),
                "confidence_score": event.get("confidence_score", 0.5),
                "is_active": event.get("is_active", True),
                "conflict_id": event.get("conflict_id")
            }
        )
    
    db.commit()


@router.post("/gdelt")
async def trigger_gdelt_collection(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Manually trigger GDELT data collection.
    
    Returns immediately, runs collection in background.
    """
    try:
        # Add timeout: 30 seconds total, 10s connect, 20s read
        collector = GDELTCollector(max_records=100, timeout=30.0)
        events = await collector.fetch()
        
        if not events:
            return {
                "status": "success",
                "message": "No new events found from GDELT",
                "count": 0
            }
        
        # Normalize events
        normalized_events = [collector.normalize(event) for event in events]
        
        # Save to database in background
        background_tasks.add_task(save_events_to_db, normalized_events, db)
        
        return {
            "status": "success",
            "message": f"Collected {len(events)} events from GDELT",
            "count": len(events)
        }
    
    except httpx.TimeoutException as e:
        logger.error(f"GDELT API timeout: {e}")
        return {
            "status": "error",
            "message": "GDELT API timeout after 30 seconds",
            "count": 0
        }
    
    except httpx.ConnectError as e:
        logger.error(f"GDELT API connection error: {e}")
        return {
            "status": "error",
            "message": "Cannot connect to GDELT API",
            "count": 0
        }
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {
            "status": "error",
            "message": f"Collection failed: {str(e)[:100]}",
            "count": 0
        }
