# AI Travel Assistant

## Project Overview
AI-powered travel planning assistant that understands user intent through conversational interface to create personalized trip recommendations.

## Core Features

### 1. Intent Understanding System
- Multi-turn conversation to extract:
  - Trip purpose (business, leisure, adventure, relaxation)
  - Travel party composition (ages, relationships, special needs)
  - Timing constraints and flexibility
  - Budget boundaries
  - Activity preferences and adventure level

### 2. User Context & Memory
- **Long-term memory**: User preferences, past trips, learned patterns
- **Session memory**: Current trip planning context
- **Key context factors**:
  - Travel party size and age groups
  - Budget level
  - Adventure level (transportation preferences)
  - Activity level (hiking, sightseeing, mobility)
  - Previous destinations and experiences

### 3. Location Intelligence
**Data Sources**:
- Google Places API (reviews, ratings)
- TripAdvisor API (tourist attractions)
- OpenWeatherMap (seasonal data)
- Local event APIs
- Flight APIs (Amadeus, Skyscanner)
- Ground transport (Rome2Rio for multi-modal routing)

**Data Categories**:
- Activity types
- Lodging options
- Food/dining
- Transportation (rental, public, walking, taxi)
- **Travel logistics**:
  - Flight pricing and availability
  - Ground transport options and costs
  - Travel duration calculations
  - Multi-modal journey planning

## Technical Architecture

### Backend Stack
- **Framework**: Python FastAPI
- **Database**: PostgreSQL with pgvector extension
  - Relational data integrity (users → trips → destinations)
  - ACID compliance for bookings/transactions
  - Native vector search with pgvector
  - Complex query support
  - JSONB for flexible data when needed
- **ORM**: SQLAlchemy
- **Validation**: Pydantic
- **Background tasks**: Celery
- **Authentication**: Google OAuth + Magic email links
- **LLM Framework**: PydanticAI
  - Type-safe conversation state
  - Native Gemini function calling
  - Structured output validation
  - Minimal overhead
- **Observability**: Langfuse
  - Free tier (50k observations/month)
  - Prompt versioning and A/B testing
  - Cost tracking and analytics
  - User feedback integration
  - Error tracking and debugging

### Frontend Stack
- **Framework**: React with TypeScript
- **Meta-framework**: Next.js
- **Styling**: TailwindCSS
- **State**: Zustand
- **Data fetching**: React Query

### Database Design
**PostgreSQL Tables**:
- Users (profile, preferences)
- Trips (past and planned)
- Conversations (chat history)
- Locations (cached destination data)

**Vector Storage** (pgvector):
- User preference embeddings
- Location description embeddings
- Activity matching vectors

### AI/LLM Strategy (Vertex AI)
**Response time target**: <10 seconds per interaction

**Model Selection**:
- **Primary**: Gemini 2.0 Flash
  - Ultra-fast responses (<2s)
  - Intent extraction
  - Follow-up questions
  - Simple clarifications
  
- **Secondary**: Gemini 2.5 Flash
  - Balance of speed and capability
  - Complex preference matching
  - Multi-destination comparisons
  
- **Advanced**: Gemini 2.5 Pro
  - Detailed itinerary generation
  - Complex constraint optimization
  - Final trip planning with all considerations

**Function Calling**:
- Native support in all Gemini 2.x models
- Parallel function execution
- Direct API integration for:
  - Flight search
  - Hotel availability
  - Weather data
  - Activity bookings

## Conversation Design

### Phase 1: Intent Discovery
- Open-ended initial prompt
- Guided questions for context gathering
- Progressive refinement

### Phase 2: Preference Refinement
- Present 3-5 curated options
- Include pros/cons and price ranges
- Show preference match scores
- Explain recommendations
- **Include travel logistics**:
  - How to get there (flight/train/drive options)
  - Total travel time
  - Estimated costs for transport

### Phase 3: Deep Planning
- Day-by-day suggestions
- Alternative activities for different party members
- Booking links and logistics
- Save/share functionality
- Transportation between activities

## User Experience Features
- Favorite/tag responses for future reference
- Support queries like:
  - "I need to plan a vacation in fall 2025 to see northern lights or beach"
  - "I'm visiting Chicago in mid July, what are cool things to do with 2 people"
- Not everyone has to do everything together
- Consider mobility and accessibility needs
- Global destination support with travel logistics
- **Component Selection System**:
  - Mark components as: chosen, considering, backup, or vetoed
  - Swap out individual activities with smart alternatives
  - Automatic backup activation for weather/closures
  - Learn from vetoed options to improve recommendations
  - Track all decisions for pattern learning

## Implementation Priorities
1. ✅ User authentication system (Google OAuth)
2. ✅ Basic UI prototype (Next.js + React)
3. ✅ Core conversation engine with mock responses
4. ✅ Database models (PostgreSQL with conversations, messages, trips)
5. ✅ Chat API endpoints
6. 🚧 Gemini AI integration (currently using mock responses)
7. ⏳ Location data integration
8. ⏳ Memory/context storage enhancements
9. ⏳ Travel logistics APIs integration
10. ⏳ Advanced features (multi-destination, group planning)

## Current Implementation Status

### Completed Features
- **Authentication**: Google OAuth 2.0 with JWT tokens
- **Database**: PostgreSQL on Google Cloud SQL with migrations
- **Backend API**: FastAPI with async support
- **Frontend**: Next.js 14 with TypeScript
- **Chat Interface**: Real-time messaging UI with starter prompts
- **Conversation Management**: State-based conversation flow
- **Data Models**: Users, Conversations, Messages, Trips
- **CI/CD Pipeline**: Complete GitHub Actions deployment workflow
- **Multi-Environment**: Dev (PR previews), Staging, Production
- **Containerization**: Docker images for both frontend and backend

### Architecture Decisions Made
- Using server-side OAuth flow for security
- Async SQLAlchemy for database operations
- Pydantic schemas for API validation
- Zustand for client state management
- Tailwind CSS for styling
- Cloud Run for serverless deployments
- Separate databases per environment
- Unique JWT secrets per environment
- Artifact Registry for Docker images

## Performance Optimization
- Pre-cache popular destinations
- Use streaming responses
- Background processing for complex queries
- Progressive enhancement
- Model selection based on query complexity

## Security & Privacy
- Secure user data storage
- API key management
- Rate limiting
- Data retention policies