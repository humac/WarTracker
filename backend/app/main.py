from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import engine, Base
import structlog

# Configure logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Note: Tables are created via Alembic migrations, not on import
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Real-time global conflict tracking and analysis platform"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    logger.info("WarTracker backend starting up")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("WarTracker backend shutting down")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to WarTracker API",
        "docs": "/docs",
        "health": "/health"
    }


# Import and include API routers (will be added as we implement them)
# from .api.v1 import events, sources, alerts, users, regions, export
# app.include_router(events.router, prefix="/api/v1", tags=["events"])
# app.include_router(sources.router, prefix="/api/v1", tags=["sources"])
# app.include_router(alerts.router, prefix="/api/v1", tags=["alerts"])
# app.include_router(users.router, prefix="/api/v1", tags=["users"])
# app.include_router(regions.router, prefix="/api/v1", tags=["regions"])
# app.include_router(export.router, prefix="/api/v1", tags=["export"])
