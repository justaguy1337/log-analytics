"""Main FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from backend.api.routes import router
from backend.config import API_HOST, API_PORT, DEBUG

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Distributed Log Analytics Platform",
    description="ML-based anomaly detection in distributed system logs",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Include routes
app.include_router(router, prefix="/api/v1", tags=["Analytics"])


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


@app.on_event("startup")
async def startup_event():
    """Startup events."""
    logger.info("Starting Distributed Log Analytics Platform")
    logger.info(f"API listening on {API_HOST}:{API_PORT}")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown events."""
    logger.info("Shutting down Log Analytics Platform")


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting server...")
    uvicorn.run(
        app,
        host=API_HOST,
        port=API_PORT,
        log_level="info" if not DEBUG else "debug"
    )
