from fastapi import FastAPI, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import logging

from app.api.v1 import api_router
from app.core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
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
        rf"^({escaped_frontend_url}|http://localhost:\d+|http://127\.0\.0\.1:\d+|https://pfm-frontend-pr-\d+-[a-zA-Z0-9]+\.us-central1\.run\.app)$"
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


# Debug middleware to log CORS details
@app.middleware("http")
async def log_cors_details(request: Request, call_next):
    """Log CORS-related details for debugging."""
    origin = request.headers.get("origin")
    if origin:
        logger.info(f"Request Origin: {origin}")
        logger.info(f"Request Method: {request.method}")
        logger.info(f"Request URL: {request.url}")
        logger.info(f"Environment: {settings.ENVIRONMENT}")
        logger.info(f"Configured Frontend URL: {settings.FRONTEND_URL}")

        if settings.ENVIRONMENT == "development":
            # Test the regex
            import re

            escaped_frontend_url = re.escape(settings.FRONTEND_URL)
            cors_regex = re.compile(
                rf"^({escaped_frontend_url}|http://localhost:\d+|http://127\.0\.0\.1:\d+|https://pfm-frontend-pr-\d+-[a-zA-Z0-9]+\.us-central1\.run\.app)$"
            )
            if cors_regex.match(origin):
                logger.info(f"Origin {origin} MATCHES CORS regex")
            else:
                logger.warning(f"Origin {origin} DOES NOT MATCH CORS regex")

    response = await call_next(request)

    # Log response CORS headers
    if origin:
        logger.info(
            f"Response Access-Control-Allow-Origin: {response.headers.get('access-control-allow-origin', 'NOT SET')}"
        )
        logger.info(
            f"Response Access-Control-Allow-Credentials: {response.headers.get('access-control-allow-credentials', 'NOT SET')}"
        )

    return response


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
