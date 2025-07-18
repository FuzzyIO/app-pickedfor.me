# PickedFor.me Backend

FastAPI backend for the AI travel planning assistant.

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up environment variables

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 3. Set up Google OAuth

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google+ API
4. Create OAuth 2.0 credentials:
   - Application type: Web application
   - Authorized redirect URIs: `http://localhost:8000/api/v1/auth/callback/google`
5. Copy Client ID and Client Secret to `.env`

### 4. Set up database

```bash
# Create PostgreSQL database
createdb pickedfor_me

# Run migrations
alembic upgrade head
```

### 5. Run the server

```bash
uvicorn app.main:app --reload
```

The API will be available at:
- API: http://localhost:8000
- Docs: http://localhost:8000/api/v1/docs
- Health: http://localhost:8000/health

## Authentication Flow

1. Frontend redirects user to `/api/v1/auth/login/google`
2. User authenticates with Google
3. Google redirects back to `/api/v1/auth/callback/google`
4. Backend creates/updates user and generates JWT
5. Backend redirects to frontend with token
6. Frontend stores token and includes in Authorization header

## API Endpoints

- `GET /api/v1/auth/login/google` - Initiate Google login
- `GET /api/v1/auth/callback/google` - Google OAuth callback
- `GET /api/v1/auth/me` - Get current user info (requires auth)
- `POST /api/v1/auth/logout` - Logout user

## Development

### Create new migration

```bash
alembic revision --autogenerate -m "Description of changes"
```

### Run tests

```bash
pytest
```