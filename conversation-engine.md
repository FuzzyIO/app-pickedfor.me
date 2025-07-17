# Conversation Engine Design

## Core Architecture

The conversation engine uses PydanticAI with a state machine pattern to manage multi-turn conversations intelligently.

## Implementation Details

### 1. State Management

```python
from enum import Enum
from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class ConversationState(Enum):
    INITIAL_INTENT = "initial_intent"
    GATHERING_CONTEXT = "gathering_context"
    REFINING_PREFERENCES = "refining_preferences"
    PRESENTING_OPTIONS = "presenting_options"
    DEEP_PLANNING = "deep_planning"
    BOOKING_ASSISTANCE = "booking_assistance"

class TravelContext(BaseModel):
    # Core trip details
    purpose: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    flexibility: Optional[str] = None  # "fixed", "flexible_dates", "flexible_duration"
    
    # Party information
    party_size: Optional[int] = None
    party_composition: List[TravelerProfile] = []
    
    # Preferences
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    adventure_level: Optional[float] = None  # 0-1 scale
    activity_preferences: List[str] = []
    
    # Constraints
    accessibility_needs: List[str] = []
    dietary_restrictions: List[str] = []
    must_have_amenities: List[str] = []
    
    # Destination preferences
    destination_type: Optional[str] = None  # "beach", "city", "nature", etc.
    climate_preference: Optional[str] = None
    preferred_regions: List[str] = []
    
    # Selected options
    selected_destination: Optional[Destination] = None
    selected_activities: List[Activity] = []
```

### 2. Conversation Flow Manager

```python
from pydantic_ai import Agent, ModelSettings
from vertexai.generative_models import GenerativeModel

class ConversationEngine:
    def __init__(self):
        self.agents = {
            'intent': Agent(
                model='gemini-2.0-flash',
                system_prompt=INTENT_EXTRACTION_PROMPT
            ),
            'context': Agent(
                model='gemini-2.5-flash',
                system_prompt=CONTEXT_GATHERING_PROMPT
            ),
            'planner': Agent(
                model='gemini-2.5-pro',
                system_prompt=TRIP_PLANNING_PROMPT
            )
        }
        
    async def process_message(
        self, 
        message: str, 
        conversation: Conversation,
        user: User
    ) -> Response:
        # 1. Update context from message
        context = await self.extract_context(message, conversation.context)
        
        # 2. Determine next state
        next_state = self.determine_state(context, conversation.state)
        
        # 3. Generate appropriate response
        response = await self.generate_response(
            state=next_state,
            context=context,
            user_memory=user.preferences
        )
        
        # 4. Execute any necessary tools
        if response.tool_calls:
            tool_results = await self.execute_tools(response.tool_calls)
            response = await self.augment_response(response, tool_results)
        
        # 5. Update conversation state
        conversation.state = next_state
        conversation.context = context
        
        return response
```

### 3. Intent Understanding

```python
INTENT_EXTRACTION_PROMPT = """
You are an expert travel planning assistant. Extract the user's travel intent from their message.

Identify:
1. Trip type (vacation, business, adventure, relaxation)
2. Urgency (planning now, future planning, just browsing)
3. Specificity (has dates/destination, general idea, completely open)
4. Key constraints mentioned

Return structured data matching the IntentClassification schema.
"""

class IntentClassification(BaseModel):
    trip_type: Optional[str]
    urgency: str
    specificity: str
    mentioned_constraints: List[str]
    needs_clarification: List[str]
```

### 4. Dynamic Question Generation

```python
class QuestionGenerator:
    def __init__(self):
        self.question_templates = {
            'party_size': [
                "Who's joining you on this adventure?",
                "Will you be traveling solo or with others?",
                "How many people are in your travel party?"
            ],
            'dates': [
                "When are you planning to travel?",
                "Do you have specific dates in mind?",
                "What time of year works best for you?"
            ],
            'budget': [
                "What's your budget range for this trip?",
                "Are you looking for budget-friendly or luxury options?",
                "What would you like to spend per person?"
            ]
        }
    
    async def get_next_question(self, context: TravelContext) -> str:
        # Identify missing critical information
        missing = self.identify_missing_info(context)
        
        # Prioritize questions based on importance
        priority = self.prioritize_questions(missing, context)
        
        # Generate contextual question
        return await self.generate_contextual_question(
            priority[0], 
            context
        )
```

### 5. Option Presentation

```python
class OptionPresenter:
    async def present_destinations(
        self, 
        context: TravelContext,
        user_preferences: UserPreferences
    ) -> List[DestinationOption]:
        # 1. Generate candidate destinations
        candidates = await self.search_destinations(context)
        
        # 2. Score based on user preferences
        scored = await self.score_destinations(
            candidates, 
            context, 
            user_preferences
        )
        
        # 3. Get travel logistics for top options
        top_5 = scored[:5]
        for dest in top_5:
            dest.travel_options = await self.get_travel_logistics(
                origin=context.origin,
                destination=dest,
                dates=context.dates
            )
        
        # 4. Format for presentation
        return self.format_options(top_5)
    
    def format_options(self, destinations: List[Destination]) -> str:
        # Create rich, scannable format with:
        # - Emoji indicators
        # - Key highlights
        # - Travel time/cost
        # - Why it matches their preferences
        pass
```

### 6. Memory Integration

```python
class MemoryManager:
    def __init__(self, db: Database):
        self.db = db
        
    async def get_user_context(self, user_id: str) -> UserMemory:
        # Fetch user preferences
        preferences = await self.db.get_user_preferences(user_id)
        
        # Get past trips for pattern learning
        past_trips = await self.db.get_user_trips(user_id)
        
        # Extract patterns
        patterns = self.extract_travel_patterns(past_trips)
        
        return UserMemory(
            preferences=preferences,
            patterns=patterns,
            past_destinations=[t.destination for t in past_trips]
        )
    
    async def update_preferences(
        self, 
        user_id: str, 
        conversation: Conversation
    ):
        # Learn from conversation
        learned = self.extract_preferences(conversation)
        
        # Update user profile
        await self.db.update_user_preferences(user_id, learned)
```

### 7. Tool Integration

```python
from pydantic_ai import Tool

# Define tools for Gemini function calling
search_flights = Tool(
    name="search_flights",
    description="Search for flights between cities",
    parameters={
        "origin": str,
        "destination": str,
        "departure_date": str,
        "return_date": str,
        "passengers": int
    }
)

search_hotels = Tool(
    name="search_hotels",
    description="Search for accommodations",
    parameters={
        "location": str,
        "check_in": str,
        "check_out": str,
        "guests": int,
        "budget_range": str
    }
)

get_activities = Tool(
    name="get_activities",
    description="Find activities and attractions",
    parameters={
        "location": str,
        "categories": List[str],
        "date": str
    }
)

# Register tools with agents
planner_agent = Agent(
    model='gemini-2.5-pro',
    tools=[search_flights, search_hotels, get_activities]
)
```

## Conversation Examples

### Example 1: Vague Initial Query

```
User: "I need a vacation"

AI: "I'd love to help you plan the perfect getaway! To find destinations that match your style, could you tell me:
- What kind of experience are you craving? (relaxation, adventure, culture)
- Roughly when are you thinking of traveling?
- Who would be joining you?"

User: "Something relaxing, maybe in October. Just me and my wife"

AI: "A relaxing October escape for two sounds wonderful! A few more details will help me find your perfect match:
- How many days are you planning to be away?
- Do you prefer beach relaxation, mountain retreats, or spa destinations?
- What's your approximate budget for the trip?"
```

### Example 2: Specific Request

```
User: "I'm visiting Chicago July 15-18 with my partner. We love food and architecture"

AI: "Chicago in July is fantastic for food and architecture lovers! Based on your interests, I've crafted some recommendations:

**Must-Do Architecture:**
🏛️ Architecture Boat Tour - See 40+ buildings from the river (2 hrs, $42/person)
🏢 Willis Tower Skydeck - Stunning views from the 103rd floor
🎨 Art Institute - Home to iconic architecture exhibits

**Food Experiences:**
🍕 Lou Malnati's - Classic deep-dish pizza
🌭 Portillo's - Chicago-style hot dogs
🍴 Girl & the Goat - Top-rated contemporary dining (book now!)

**Perfect Combo:**
Day 1: Architecture boat tour → Lunch at Portillo's → Millennium Park
Day 2: Art Institute → Pizza at Lou's → Riverwalk stroll

Should I create a detailed day-by-day itinerary with reservations info?"
```

## Performance Optimizations

1. **Response Streaming**: Use Gemini's streaming capability for perceived faster responses
2. **Parallel Tool Calls**: Execute multiple API calls simultaneously
3. **Smart Caching**: Cache destination data, common routes, seasonal information
4. **Progressive Enhancement**: Show partial results while fetching additional details
5. **Model Routing**: Use Gemini 2.0 Flash for simple queries, upgrade to 2.5 Pro for complex planning

## Error Handling

```python
class ConversationErrorHandler:
    async def handle_error(self, error: Exception, context: Context):
        if isinstance(error, APITimeoutError):
            return "I'm gathering that information - one moment please..."
        
        elif isinstance(error, NoResultsError):
            return await self.suggest_alternatives(context)
        
        elif isinstance(error, InvalidDateError):
            return "Those dates might not work - could you check them?"
        
        else:
            # Log error for debugging
            await self.log_error(error, context)
            return "Let me try a different approach..."
```

This architecture provides a robust, scalable conversation engine that can handle complex travel planning queries while maintaining context and learning from user interactions.