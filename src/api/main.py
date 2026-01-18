"""
Main API application for huquqAI system
FastAPI REST API endpoints
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from loguru import logger

from src.core.config import get_config
from src.api.routes import router
from src.utils.logger import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting huquqAI application...")
    setup_logging()
    logger.info("huquqAI started successfully")

    yield

    # Shutdown
    logger.info("Shutting down huquqAI application...")


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    config = get_config()

    app = FastAPI(
        title="huquqAI API",
        description="Legal Knowledge Base System for Karakalpak Language",
        version=config.application.get("version", "0.1.0"),
        lifespan=lifespan
    )

    # CORS middleware
    if config.api.cors.get("enabled", True):
        app.add_middleware(
            CORSMiddleware,
            allow_origins=config.api.cors.get("origins", ["*"]),
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Include routers
    app.include_router(router, prefix="/api/v1")

    return app


app = create_app()


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "huquqAI",
        "description": "Qalpaq tili ushın huqıqlıq bilimler bazası",
        "version": "0.1.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


def main():
    """Main entry point"""
    import uvicorn
    config = get_config()

    uvicorn.run(
        "src.api.main:app",
        host=config.api.host,
        port=config.api.port,
        reload=config.api.reload,
        workers=config.api.workers
    )


if __name__ == "__main__":
    main()
