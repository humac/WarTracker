from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.database import get_db
from app.models import Alert
import structlog

logger = structlog.get_logger()

router = APIRouter()


@router.get("")
async def list_alerts(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    """List all alerts."""
    try:
        query = db.query(Alert)
        
        if active_only:
            query = query.filter(Alert.is_active == True)
        
        alerts = query.order_by(Alert.created_at.desc()).offset(skip).limit(limit).all()
        
        return {
            "alerts": alerts,
            "total": len(alerts)
        }
    except Exception as e:
        logger.error("Error listing alerts", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{alert_id}")
async def get_alert(alert_id: int, db: Session = Depends(get_db)):
    """Get details for a specific alert."""
    try:
        alert = db.query(Alert).filter(Alert.id == alert_id).first()
        
        if not alert:
            raise HTTPException(status_code=404, detail="Alert not found")
        
        return alert
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error getting alert", alert_id=alert_id, error=str(e))
        raise HTTPException(status_code=500, detail=str(e))
