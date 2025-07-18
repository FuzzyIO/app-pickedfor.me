from datetime import datetime
from typing import Optional

from authlib.integrations.httpx_client import AsyncOAuth2Client
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import create_access_token
from app.models.user import User
from app.schemas.user import UserCreate


class GoogleOAuth:
    """Handle Google OAuth authentication."""

    def __init__(self):
        self.client = AsyncOAuth2Client(
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            redirect_uri=settings.GOOGLE_REDIRECT_URI,
        )
        self.authorize_url = "https://accounts.google.com/o/oauth2/v2/auth"
        self.token_url = "https://oauth2.googleapis.com/token"
        self.userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"

    def get_authorization_url(self) -> str:
        """Get the Google OAuth authorization URL."""
        authorization_url, _ = self.client.create_authorization_url(
            self.authorize_url,
            scope="openid email profile",
            access_type="offline",
            prompt="select_account",
        )
        return authorization_url

    async def get_access_token(self, code: str) -> dict:
        """Exchange authorization code for access token."""
        token = await self.client.fetch_token(
            self.token_url,
            authorization_response=f"{settings.GOOGLE_REDIRECT_URI}?code={code}",
            code=code,
        )
        return token

    async def get_user_info(self, token: dict) -> dict:
        """Get user information from Google."""
        self.client.token = token
        resp = await self.client.get(self.userinfo_url)
        resp.raise_for_status()
        return resp.json()


class AuthService:
    """Handle user authentication and management."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.google_oauth = GoogleOAuth()

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_user_by_google_id(self, google_id: str) -> Optional[User]:
        """Get user by Google ID."""
        result = await self.db.execute(select(User).where(User.google_id == google_id))
        return result.scalar_one_or_none()

    async def create_user(self, user_data: UserCreate) -> User:
        """Create a new user."""
        user = User(
            email=user_data.email,
            full_name=user_data.full_name,
            google_id=user_data.google_id,
            profile_picture=user_data.profile_picture,
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def authenticate_google_user(self, code: str) -> tuple[User, str]:
        """Authenticate user with Google OAuth code."""
        # Exchange code for token
        token = await self.google_oauth.get_access_token(code)

        # Get user info from Google
        user_info = await self.google_oauth.get_user_info(token)

        # Check if user exists
        user = await self.get_user_by_google_id(user_info["id"])

        if not user:
            # Check by email
            user = await self.get_user_by_email(user_info["email"])

            if user:
                # Update existing user with Google ID
                user.google_id = user_info["id"]
                user.profile_picture = user_info.get("picture")
                user.full_name = user_info.get("name", user.full_name)
            else:
                # Create new user
                user_data = UserCreate(
                    email=user_info["email"],
                    full_name=user_info.get("name"),
                    google_id=user_info["id"],
                    profile_picture=user_info.get("picture"),
                )
                user = await self.create_user(user_data)

        # Update last login
        user.last_login = datetime.utcnow()
        await self.db.commit()

        # Create access token
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email}
        )

        return user, access_token
