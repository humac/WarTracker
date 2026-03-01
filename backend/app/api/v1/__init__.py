from fastapi import APIRouter
from . import events, sources, alerts

api_router = APIRouter()

api_router.include_router(events.router, prefix="/events", tags=["events"])
api_router.include_router(sources.router, prefix="/sources", tags=["sources"])
api_router.include_router(alerts.router, prefix="/alerts", tags=["alerts"])
