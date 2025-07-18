# PickedFor.me Architecture Documentation

## System Architecture Overview

```mermaid
graph TB
    subgraph "Client Layer"
        UI[React/Next.js Frontend]
        Mobile[Mobile Web App]
    end
    
    subgraph "API Gateway"
        APIGW[FastAPI Gateway]
        Auth[Auth Service]
    end
    
    subgraph "Core Services"
        CE[Conversation Engine]
        MM[Memory Manager]
        LS[Location Service]
        TS[Travel Service]
    end
    
    subgraph "AI Layer"
        Gemini[Vertex AI Gemini]
        Embeddings[Text Embeddings]
    end
    
    subgraph "Data Layer"
        PG[(PostgreSQL)]
        Redis[(Redis Cache)]
        Vector[(pgvector)]
    end
    
    subgraph "External APIs"
        Google[Google APIs]
        Flight[Flight APIs]
        Hotel[Hotel APIs]
        Transport[Transport APIs]
    end
    
    UI --> APIGW
    Mobile --> APIGW
    APIGW --> Auth
    APIGW --> CE
    
    CE --> MM
    CE --> LS
    CE --> TS
    CE --> Gemini
    
    MM --> PG
    MM --> Vector
    MM --> Redis
    
    LS --> Google
    LS --> Redis
    
    TS --> Flight
    TS --> Hotel
    TS --> Transport
    
    Embeddings --> Vector
```

## Conversation Engine Architecture

```mermaid
stateDiagram-v2
    [*] --> InitialIntent
    InitialIntent --> GatheringContext
    GatheringContext --> RefiningPreferences
    RefiningPreferences --> PresentingOptions
    PresentingOptions --> DeepPlanning
    PresentingOptions --> RefiningPreferences
    DeepPlanning --> BookingAssistance
    BookingAssistance --> [*]
    
    GatheringContext --> GatheringContext : Need More Info
    RefiningPreferences --> GatheringContext : Missing Context
```

## Data Schema

```mermaid
erDiagram
    User ||--o{ Trip : plans
    User ||--o{ Conversation : has
    User ||--|| UserPreference : has
    Trip ||--o{ TripDay : contains
    Trip ||--o{ TripMember : includes
    Trip }o--|| Destination : visits
    Trip ||--o{ ComponentDecision : tracks
    Conversation ||--o{ Message : contains
    Message ||--o{ MessageContext : tracks
    Destination ||--o{ Activity : offers
    Destination ||--o{ Accommodation : has
    ComponentDecision ||--o{ ComponentAlternative : maps
    User ||--o{ DecisionPattern : learns
    
    User {
        uuid id PK
        string email
        string name
        jsonb auth_data
        timestamp created_at
    }
    
    UserPreference {
        uuid id PK
        uuid user_id FK
        float adventure_level
        string budget_preference
        jsonb dietary_restrictions
        jsonb accessibility_needs
        vector preference_embedding
    }
    
    Trip {
        uuid id PK
        uuid user_id FK
        string status
        date start_date
        date end_date
        jsonb party_composition
        decimal budget_min
        decimal budget_max
        uuid destination_id FK
    }
    
    Conversation {
        uuid id PK
        uuid user_id FK
        uuid trip_id FK
        string state
        jsonb context
        timestamp started_at
        timestamp last_active
    }
    
    Message {
        uuid id PK
        uuid conversation_id FK
        string role
        text content
        jsonb function_calls
        timestamp created_at
    }
    
    Destination {
        uuid id PK
        string name
        point coordinates
        jsonb metadata
        vector description_embedding
    }
    
    ComponentDecision {
        uuid id PK
        uuid trip_id FK
        uuid user_id FK
        string component_type
        uuid component_id
        string decision
        text reason
        timestamp decided_at
    }
    
    ComponentAlternative {
        uuid id PK
        uuid trip_id FK
        uuid primary_component_id
        uuid backup_component_id
        integer priority
        string activation_reason
    }
    
    DecisionPattern {
        uuid id PK
        uuid user_id FK
        string pattern_type
        jsonb pattern_data
        float confidence
        timestamp learned_at
    }
```

## Conversation Flow Implementation

```mermaid
sequenceDiagram
    participant User
    participant API
    participant ConvEngine
    participant Memory
    participant LLM
    participant Tools
    
    User->>API: Send message
    API->>ConvEngine: Process request
    ConvEngine->>Memory: Get user context
    Memory-->>ConvEngine: Context data
    
    ConvEngine->>LLM: Generate with context
    LLM-->>ConvEngine: Intent + Next action
    
    alt Needs Information
        ConvEngine->>User: Ask clarifying question
    else Needs Data
        ConvEngine->>Tools: Call external APIs
        Tools-->>ConvEngine: API results
        ConvEngine->>LLM: Generate with data
        LLM-->>ConvEngine: Response
    else Ready to Present
        ConvEngine->>User: Show options
    end
    
    ConvEngine->>Memory: Update context
```

## Application Workflow

```mermaid
flowchart TD
    Start([User Opens App]) --> Auth{Authenticated?}
    Auth -->|No| Login[Login/Signup]
    Auth -->|Yes| Home[Home Screen]
    Login --> Home
    
    Home --> NewTrip[Start New Trip]
    Home --> PastTrips[View Past Trips]
    Home --> Prefs[Update Preferences]
    
    NewTrip --> Intent[Express Intent]
    Intent --> AI{AI Processing}
    
    AI -->|Need Context| Questions[Ask Questions]
    Questions --> AI
    
    AI -->|Ready| Options[Present Options]
    Options --> Select{User Selects}
    
    Select -->|Refine| AI
    Select -->|Accept| Planning[Deep Planning]
    
    Planning --> Itinerary[Day-by-day Plan]
    Itinerary --> Save[Save Trip]
    Itinerary --> Book[Booking Links]
```

## Memory Architecture

```mermaid
graph LR
    subgraph "Memory Types"
        STM[Short-term Memory<br/>Current Session]
        LTM[Long-term Memory<br/>User Preferences]
        ETM[Episodic Memory<br/>Past Trips]
    end
    
    subgraph "Storage"
        Cache[Redis Cache]
        DB[(PostgreSQL)]
        Vectors[(pgvector)]
    end
    
    STM --> Cache
    LTM --> DB
    LTM --> Vectors
    ETM --> DB
    ETM --> Vectors
    
    subgraph "Retrieval"
        Similar[Similarity Search]
        Filters[Attribute Filters]
        Ranking[Relevance Ranking]
    end
    
    Vectors --> Similar
    DB --> Filters
    Similar --> Ranking
    Filters --> Ranking
```

## API Structure

### Implemented Endpoints

```yaml
/api/v1/:
  /auth:
    GET /login/google          # Initiate Google OAuth
    GET /callback/google        # Handle OAuth callback
    POST /callback/google       # API callback for mobile
    GET /me                     # Get current user
    POST /logout               # Logout user
    
  /chat:
    GET /conversations         # List user conversations
    GET /conversations/{id}    # Get conversation with messages
    POST /conversations        # Create new conversation
    PATCH /conversations/{id}  # Update conversation
    DELETE /conversations/{id} # Delete conversation
    POST /chat                 # Send message and get response
```

### Planned Endpoints

```yaml
/api/v1/:
  /trips:
    GET /                      # List user trips
    GET /{trip_id}            # Get trip details
    POST /                    # Create trip
    PUT /{trip_id}            # Update trip
    DELETE /{trip_id}         # Delete trip
    
  /destinations:
    GET /search               # Search destinations
    GET /{destination_id}     # Get destination details
    GET /{destination_id}/activities  # Get activities
    
  /users:
    GET /preferences          # Get user preferences
    PUT /preferences          # Update preferences
    GET /history             # Get user history
```

## Security Architecture

```mermaid
graph TB
    subgraph "Security Layers"
        WAF[Web Application Firewall]
        RateLimit[Rate Limiting]
        Auth[Authentication]
        AuthZ[Authorization]
        Encrypt[Encryption]
    end
    
    Client[Client] --> WAF
    WAF --> RateLimit
    RateLimit --> Auth
    Auth --> AuthZ
    AuthZ --> API[API Endpoints]
    
    API <--> Encrypt
    Encrypt <--> DB[(Database)]
```

## Deployment Architecture

```mermaid
graph TB
    subgraph "Google Cloud Platform"
        subgraph "Frontend"
            CDN[Cloud CDN]
            LB[Load Balancer]
            CR[Cloud Run - Next.js]
        end
        
        subgraph "Backend"
            APILB[API Load Balancer]
            APIRun[Cloud Run - FastAPI]
            Workers[Cloud Run Jobs - Workers]
        end
        
        subgraph "Data"
            SQL[Cloud SQL - PostgreSQL]
            Memstore[Memorystore - Redis]
        end
        
        subgraph "AI"
            Vertex[Vertex AI]
        end
    end
    
    Users[Users] --> CDN
    CDN --> LB
    LB --> CR
    CR --> APILB
    APILB --> APIRun
    APIRun --> SQL
    APIRun --> Memstore
    APIRun --> Vertex
    APIRun --> Workers
```

## Implementation Status

### ✅ Completed Components

1. **Authentication System**
   - Google OAuth 2.0 integration
   - JWT token-based authentication
   - User session management
   - Protected API endpoints

2. **Database Layer**
   - Google Cloud SQL PostgreSQL instance
   - SQLAlchemy async ORM setup
   - Alembic migrations
   - Models: User, Conversation, Message, Trip

3. **Backend API**
   - FastAPI application structure
   - Async request handling
   - Pydantic schemas for validation
   - CORS configuration

4. **Frontend Application**
   - Next.js 14 with TypeScript
   - Tailwind CSS styling
   - Authentication flow
   - Chat interface components

5. **Chat System**
   - Conversation state management
   - Message history
   - Mock AI responses based on state
   - Real-time UI updates

### 🚧 In Progress

1. **Gemini AI Integration**
   - Replace mock responses with actual AI
   - Implement function calling
   - Add streaming responses

2. **WebSocket Support**
   - Real-time message updates
   - Typing indicators
   - Connection management

### ⏳ Planned Components

1. **Memory System**
   - User preference learning
   - Context persistence
   - pgvector integration

2. **Location Services**
   - Google Places integration
   - Destination search
   - Activity recommendations

3. **Travel Services**
   - Flight search integration
   - Hotel availability
   - Transport options

4. **Advanced Features**
   - Multi-destination planning
   - Group coordination
   - Booking assistance