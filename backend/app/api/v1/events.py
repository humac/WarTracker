from fastapi import APIRouter, Depends, HTTPException, Query, Request
from app.rate_limiter import limiter
from sqlalchemy.orm import Session
from sqlalchemy import text, func
from typing import List, Optional, Dict, Any
from datetime import datetime
from app.database import get_db
from app.models import ConflictEvent
import structlog

logger = structlog.get_logger()

router = APIRouter()


@router.get("")
@limiter.limit("100/minute")
async def list_events(
    request: Request,
    lat: Optional[float] = Query(None, description="Latitude for geospatial query"),
    lon: Optional[float] = Query(None, description="Longitude for geospatial query"),
    radius: Optional[float] = Query(50, description="Radius in kilometers"),
    severity: Optional[int] = Query(None, ge=1, le=5, description="Filter by severity level"),
    date_from: Optional[datetime] = Query(None, description="Start date filter"),
    date_to: Optional[datetime] = Query(None, description="End date filter"),
    source: Optional[str] = Query(None, description="Filter by source ID"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
    db: Session = Depends(get_db)
):
    """
    List conflict events with optional filters.
    Supports geospatial queries (lat/lon/radius).
    """
    try:
        query = db.query(ConflictEvent)
        
        # Geospatial filter
        if lat is not None and lon is not None:
            # Convert radius from km to meters
            radius_meters = radius * 1000
            query = query.filter(
                text(
                    "ST_DWithin(location, ST_MakePoint(:lon, :lat)::geography, :radius)"
                )
            ).params(lon=lon, lat=lat, radius=radius_meters)
        
        # Severity filter
        if severity is not None:
            query = query.filter(ConflictEvent.severity == severity)
        
        # Date range filters
        if date_from is not None:
            query = query.filter(ConflictEvent.event_timestamp >= date_from)
        if date_to is not None:
            query = query.filter(ConflictEvent.event_timestamp <= date_to)
        
        # Source filter
        if source is not None:
            query = query.filter(ConflictEvent.source_id == source)
        
        # Order by most recent first
        query = query.order_by(ConflictEvent.event_timestamp.desc())
        
        # Pagination
        events = query.offset(skip).limit(limit).all()
        
        # Manually serialize events (PostGIS geometry needs special handling)
        serialized_events = []
        for event in events:
            event_dict = {
                "id": event.id,
                "title": event.title,
                "description": event.description,
                "event_type": event.event_type,
                "severity_score": event.severity_score,
                "event_timestamp": event.event_timestamp.isoformat() if event.event_timestamp else None,
                "verification_status": event.verification_status,
                "confidence_score": event.confidence_score,
                "country_code": event.country_code,
                "region_name": event.region_name,
                "is_active": event.is_active,
                "conflict_id": event.conflict_id,
                # Extract lat/lon from PostGIS geometry
                "latitude": None,
                "longitude": None
            }
            
            # Convert PostGIS geometry to lat/lon
            if event.location:
                try:
                    # Query to extract coordinates
                    result = db.execute(
                        text("SELECT ST_Y(location), ST_X(location) FROM conflict_events WHERE id = :id"),
                        {"id": event.id}
                    ).first()
                    if result:
                        event_dict["latitude"] = result[0]
                        event_dict["longitude"] = result[1]
                except Exception:
                    pass
            
            serialized_events.append(event_dict)
        
        return {
            "events": serialized_events,
            "total": len(serialized_events),
            "skip": skip,
            "limit": limit
        }
    except Exception as e:
        logger.error("Error listing events", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{event_id}")
@limiter.limit("100/minute")
async def get_event(request: Request, event_id: int, db: Session = Depends(get_db)):
    """Get detailed information about a specific conflict event."""
    try:
        event = db.query(ConflictEvent).filter(ConflictEvent.id == event_id).first()
        
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        return event
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error getting event", event_id=event_id, error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
@limiter.limit("100/minute")
async def get_stats(
    request: Request,
    date_from: Optional[datetime] = Query(None, description="Start date for statistics"),
    date_to: Optional[datetime] = Query(None, description="End date for statistics"),
    db: Session = Depends(get_db)
):
    """
    Get aggregated statistics:
    - Total events
    - Events by severity
    - Events by region
    - Events by source
    - Timeline (events per day)
    """
    try:
        # Base query with optional date filters
        base_query = db.query(ConflictEvent)
        if date_from:
            base_query = base_query.filter(ConflictEvent.event_timestamp >= date_from)
        if date_to:
            base_query = base_query.filter(ConflictEvent.event_timestamp <= date_to)
        
        # Total events
        total_events = base_query.count()
        
        # Events by severity
        severity_stats = db.query(
            ConflictEvent.severity,
            func.count(ConflictEvent.id).label('count')
        ).group_by(ConflictEvent.severity).all()
        events_by_severity = {
            f"severity_{s.severity}": s.count for s in severity_stats if s.severity is not None
        }
        
        # Events by source
        source_stats = db.query(
            ConflictEvent.source_id,
            func.count(ConflictEvent.id).label('count')
        ).group_by(ConflictEvent.source_id).all()
        events_by_source = {
            s.source_id: s.count for s in source_stats if s.source_id is not None
        }
        
        # Timeline (events per day)
        timeline_stats = db.query(
            func.date(ConflictEvent.event_timestamp).label('date'),
            func.count(ConflictEvent.id).label('count')
        ).group_by(func.date(ConflictEvent.event_timestamp)).order_by(
            func.date(ConflictEvent.event_timestamp)
        ).all()
        timeline = {
            str(t.date): t.count for t in timeline_stats
        }
        
        # Events by region (using ST_AsText for region identification)
        # This is a simplified approach - in production, you'd use proper region boundaries
        region_stats = db.query(
            func.ST_AsText(ConflictEvent.location).label('location'),
            func.count(ConflictEvent.id).label('count')
        ).group_by(func.ST_AsText(ConflictEvent.location)).limit(10).all()
        
        return {
            "total_events": total_events,
            "events_by_severity": events_by_severity,
            "events_by_source": events_by_source,
            "timeline": timeline,
            "date_range": {
                "from": date_from.isoformat() if date_from else None,
                "to": date_to.isoformat() if date_to else None
            }
        }
    except Exception as e:
        logger.error("Error getting stats", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))
