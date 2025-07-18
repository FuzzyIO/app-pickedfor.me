# PickedFor.me - AI Travel Planning Assistant

An intelligent travel planning application that understands user intent through conversational AI to create personalized trip recommendations.

## 🚀 Project Overview

PickedFor.me uses advanced AI to have natural conversations with users about their travel preferences, understanding not just where they want to go, but why they're traveling, who they're with, and what experiences they're seeking. The app learns from user choices to provide increasingly personalized recommendations.

## 📚 Documentation

- **[Project Planning & Architecture](./CLAUDE.md)** - Core features, technical decisions, and system design
- **[System Architecture](./architecture.md)** - Detailed architecture diagrams and data flow
- **[Conversation Engine Design](./conversation-engine.md)** - AI conversation flow and implementation
- **[Component Selection System](./component-selection-system.md)** - Trip component decision tracking and learning
- **[LLM Observability](./llm-observability.md)** - Monitoring and optimization strategy

## 🏗️ Project Structure

```
pickedfor.me/
├── backend/          # FastAPI backend with Python
│   ├── app/         # Application code
│   ├── migrations/  # Database migrations
│   └── README.md    # Backend setup instructions
├── frontend/        # Next.js frontend with TypeScript
│   ├── src/         # React components and pages
│   └── README.md    # Frontend setup instructions
└── docs/           # Additional documentation
```

## 🚦 Current Status

✅ **Completed**:
- Google OAuth authentication system
- User management with PostgreSQL (Cloud SQL)
- Protected routes and session management
- Chat interface with real-time messaging
- Conversation state management
- Database models for trips and messages
- Mock AI responses based on conversation state

🚧 **In Progress**:
- Vertex AI Gemini integration
- PydanticAI implementation
- WebSocket support for real-time updates

📋 **Planned**:
- Travel API integrations (flights, hotels, activities)
- Component selection UI
- Real-time adaptation system
- Memory and preference learning
- pgvector integration for semantic search

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL with pgvector extension
- **Authentication**: Google OAuth 2.0
- **AI Framework**: PydanticAI (planned)
- **Observability**: Langfuse (planned)

### Frontend
- **Framework**: Next.js 14 with TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **Data Fetching**: React Query

### AI/ML
- **LLM Provider**: Google Vertex AI
- **Models**: Gemini 2.0 Flash, 2.5 Flash, 2.5 Pro
- **Embeddings**: pgvector for semantic search

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Node.js 18+
- PostgreSQL (local or Cloud SQL)
- Google Cloud Project with OAuth configured

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env      # Add your credentials
alembic upgrade head
uvicorn app.main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Visit http://localhost:3000 to see the app!

## 📡 API Endpoints

### Authentication
- `GET /api/v1/auth/login/google` - Initiate Google OAuth
- `GET /api/v1/auth/me` - Get current user info
- `POST /api/v1/auth/logout` - Logout

### Chat
- `POST /api/v1/chat/chat` - Send message and get AI response
- `GET /api/v1/chat/conversations` - List user conversations
- `GET /api/v1/chat/conversations/{id}` - Get conversation with messages
- `POST /api/v1/chat/conversations` - Create new conversation

## 🔑 Key Features

### Intelligent Conversation
- Natural language understanding of travel intent
- Multi-turn conversations to gather context
- Learns from user preferences over time

### Smart Planning
- **Component Selection**: Choose, veto, or keep as backup individual trip components
- **Automatic Adaptation**: Adjusts plans for weather, closures, or changes
- **Group Planning**: Different activities for different party members

### Travel Logistics
- Flight and transportation options
- Accommodation recommendations
- Real-time pricing and availability
- Multi-modal journey planning

## 🧪 Development

### Running Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Code Quality
```bash
# Backend
black .
ruff check .

# Frontend
npm run lint
```

## 📈 Monitoring

The app includes comprehensive observability:
- Request tracing with Langfuse
- Cost tracking per conversation
- Quality metrics and user satisfaction
- A/B testing for prompt optimization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is proprietary and confidential.

## 🙏 Acknowledgments

- Built with Google Cloud Platform
- Powered by Gemini AI models
- Authentication via Google OAuth

---

**Note**: This is an active development project. Features and documentation are continuously evolving.