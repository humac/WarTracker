from fastapi import APIRouter, Depends, HTTPException, Request
from app.rate_limiter import limiter
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Source
from datetime import datetime
import structlog

logger = structlog.get_logger()

router = APIRouter()


@router.get("")
@limiter.limit("100/minute")
async def list_sources(request: Request, db: Session = Depends(get_db)):
    """List all configured data sources with status."""
    try:
        sources = db.query(Source).all()
        
        return {
            "sources": sources,
            "total": len(sources)
        }
    except Exception as e:
        logger.error("Error listing sources", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{source_id}")
@limiter.limit("100/minute")
async def get_source(request: Request, source_id: str, db: Session = Depends(get_db)):
    """Get details for a specific data source."""
    try:
        source = db.query(Source).filter(Source.id == source_id).first()
        
        if not source:
            raise HTTPException(status_code=404, detail="Source not found")
        
        return source
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error getting source", source_id=source_id, error=str(e))
        raise HTTPException(status_code=500, detail=str(e))
