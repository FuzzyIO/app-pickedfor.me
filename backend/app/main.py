from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import logging

from app.api.v1 import api_router
from app.core.config import settings

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Set up CORS
# For development, allow localhost origins
allowed_origins = [settings.FRONTEND_URL]
if settings.ENVIRONMENT == "development":
    allowed_origins.extend(
        [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:3001",
            "http://127.0.0.1:3001",
        ]
    )

# Log the allowed origins for debugging
logger.info(f"CORS allowed origins: {allowed_origins}")
logger.info(f"Frontend URL from settings: {settings.FRONTEND_URL}")
logger.info(f"Environment: {settings.ENVIRONMENT}")

# Use regex pattern for PR preview URLs in development
if settings.ENVIRONMENT == "development":
    import re

    # Allow PR preview URLs and localhost
    # This regex allows localhost, 127.0.0.1, PR preview URLs, and the configured frontend URL
    escaped_frontend_url = re.escape(settings.FRONTEND_URL)
    cors_regex = re.compile(
        rf"^({escaped_frontend_url}|http://localhost:\d+|http://127\.0\.0\.1:\d+|https://pfm-frontend-pr-\d+-.*\.a\.run\.app)$"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=cors_regex,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} API",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    from sqlalchemy import text
    from app.core.database import engine

    try:
        # Test database connection
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
            await conn.commit()

        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unhealthy",
                "database": "disconnected",
                "error": str(e),
            },
        )
