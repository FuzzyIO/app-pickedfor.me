# PickedFor.me Frontend

Next.js frontend for the AI travel planning assistant.

## Setup

### 1. Install dependencies

```bash
npm install
```

### 2. Configure environment

The `.env.local` file is already configured for local development:
- API URL: http://localhost:8000/api/v1
- App URL: http://localhost:3000

### 3. Run the development server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Features

- **Google OAuth Authentication**: Seamless login with Google
- **Protected Routes**: Automatic redirect for authenticated pages
- **Responsive Design**: Built with Tailwind CSS
- **State Management**: Zustand for auth state persistence
- **API Integration**: Axios with automatic auth token handling

## Project Structure

```
src/
├── app/                 # Next.js app directory
│   ├── login/          # Login page
│   ├── dashboard/      # Protected dashboard
│   └── auth/callback/  # OAuth callback handler
├── components/         # Reusable components
├── hooks/             # Custom React hooks
├── lib/               # Utilities and API client
├── store/             # Zustand stores
└── types/             # TypeScript types
```

## Authentication Flow

1. User clicks "Continue with Google" on login page
2. Redirected to Google OAuth consent screen
3. Google redirects back to `/api/v1/auth/callback/google`
4. Backend validates and redirects to `/auth/callback?token=...`
5. Frontend stores token and fetches user data
6. User redirected to dashboard

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

## Next Steps

1. Add trip planning interface
2. Implement chat-based conversation
3. Add trip history and management
4. Build component selection UI
5. Add real-time updates