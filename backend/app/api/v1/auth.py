from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.schemas.user import Token, User
from app.services.auth import AuthService
from app.api.deps import get_current_user

router = APIRouter()


@router.get("/login/google")
async def google_login():
    """Initiate Google OAuth login."""
    auth_service = AuthService(None)  # No DB needed for this
    auth_url = auth_service.google_oauth.get_authorization_url()
    return {"auth_url": auth_url}


@router.get("/callback/google")
async def google_callback(
    code: str = Query(..., description="Authorization code from Google"),
    db: AsyncSession = Depends(get_db)
):
    """Handle Google OAuth callback."""
    try:
        auth_service = AuthService(db)
        user, access_token = await auth_service.authenticate_google_user(code)
        
        # Redirect to frontend with token
        redirect_url = f"{settings.FRONTEND_URL}/auth/callback?token={access_token}"
        return RedirectResponse(url=redirect_url)
        
    except Exception as e:
        # Redirect to frontend with error
        redirect_url = f"{settings.FRONTEND_URL}/auth/error?message={str(e)}"
        return RedirectResponse(url=redirect_url)


@router.post("/callback/google", response_model=Token)
async def google_callback_api(
    code: str,
    db: AsyncSession = Depends(get_db)
):
    """Handle Google OAuth callback via API (for mobile apps)."""
    try:
        auth_service = AuthService(db)
        user, access_token = await auth_service.authenticate_google_user(code)
        
        return Token(access_token=access_token)
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Authentication failed: {str(e)}"
        )


@router.get("/me", response_model=User)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """Get current user information."""
    return current_user


@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user)
):
    """Logout current user."""
    # For JWT, we just return success
    # The client should remove the token
    return {"message": "Successfully logged out"}