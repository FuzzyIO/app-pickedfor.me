# Trip Component Selection & Feedback System

## Overview

The component selection system allows users to fine-tune their itinerary by marking individual components with different decision states. This creates a learning system that improves recommendations over time.

## Component Decision States

```python
from enum import Enum

class ComponentDecision(Enum):
    CHOSEN = "chosen"              # ✅ Definitely doing this
    CONSIDERING = "considering"     # 🤔 Maybe, still thinking
    BACKUP = "backup"              # 📌 Good alternative option
    VETOED = "vetoed"              # ❌ Definitely not
    COMPLETED = "completed"        # ✓ Already done
    MISSED = "missed"              # ⚠️ Couldn't do (closed, weather, etc.)
```

## Data Model

### Enhanced Database Schema

```sql
-- Component decisions tracking
CREATE TABLE component_decisions (
    id UUID PRIMARY KEY,
    trip_id UUID REFERENCES trips(id),
    user_id UUID REFERENCES users(id),
    component_type VARCHAR(50), -- 'activity', 'restaurant', 'hotel', 'transport'
    component_id UUID,
    decision ComponentDecision,
    reason TEXT,
    decided_at TIMESTAMP,
    metadata JSONB -- store details like weather impact, closure, etc.
);

-- Backup mapping for alternatives
CREATE TABLE component_alternatives (
    id UUID PRIMARY KEY,
    trip_id UUID REFERENCES trips(id),
    primary_component_id UUID,
    backup_component_id UUID,
    priority INTEGER,
    activation_reason TEXT -- 'weather', 'closure', 'timing', etc.
);

-- Learning from decisions
CREATE TABLE decision_patterns (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    pattern_type VARCHAR(50),
    pattern_data JSONB,
    confidence FLOAT,
    learned_at TIMESTAMP
);
```

### Component Structure

```python
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

class TripComponent(BaseModel):
    id: str
    type: str  # 'activity', 'restaurant', 'hotel', 'transport'
    name: str
    description: str
    location: Location
    timing: TimeSlot
    price_range: PriceRange
    tags: List[str]
    weather_dependent: bool
    booking_required: bool
    
class ComponentWithDecision(TripComponent):
    decision: ComponentDecision
    decision_reason: Optional[str]
    decided_at: Optional[datetime]
    alternatives: List[TripComponent]
    swap_suggestions: List[TripComponent]
    
class ItineraryDay(BaseModel):
    date: datetime
    components: List[ComponentWithDecision]
    backup_components: List[TripComponent]
    weather_contingency: Optional[List[TripComponent]]
```

## User Interface Design

### Component Selection UI

```typescript
interface ComponentCard {
  component: TripComponent;
  decision: ComponentDecision;
  onDecisionChange: (decision: ComponentDecision) => void;
  onSwapRequest: () => void;
  alternatives: TripComponent[];
}

// Visual representation
const DecisionButtons = () => (
  <div className="decision-buttons">
    <button className="chosen" title="Definitely doing this">
      ✅ Yes
    </button>
    <button className="considering" title="Still thinking">
      🤔 Maybe
    </button>
    <button className="backup" title="Good backup option">
      📌 Backup
    </button>
    <button className="vetoed" title="Not interested">
      ❌ No
    </button>
    <button className="swap" title="Show me alternatives">
      🔄 Swap
    </button>
  </div>
);
```

### Swap Interface

```python
class SwapRecommendationEngine:
    async def get_swap_suggestions(
        self,
        component: TripComponent,
        context: TripContext,
        user_decisions: List[ComponentDecision]
    ) -> List[TripComponent]:
        # 1. Understand why user wants to swap
        swap_reason = await self.infer_swap_reason(component, user_decisions)
        
        # 2. Filter out vetoed types
        vetoed_patterns = self.extract_vetoed_patterns(user_decisions)
        
        # 3. Find alternatives that:
        #    - Fit the time slot
        #    - Match chosen component patterns
        #    - Avoid vetoed patterns
        #    - Are geographically convenient
        
        alternatives = await self.search_alternatives(
            time_slot=component.timing,
            location_near=component.location,
            match_patterns=self.extract_chosen_patterns(user_decisions),
            avoid_patterns=vetoed_patterns
        )
        
        # 4. Rank by likelihood of acceptance
        ranked = self.rank_by_user_preferences(alternatives, user_decisions)
        
        return ranked[:5]
```

## Decision Learning System

```python
class DecisionLearningEngine:
    def __init__(self):
        self.patterns = {
            'activity_type': {},      # outdoor vs indoor
            'price_sensitivity': {},  # budget patterns
            'timing_preference': {},  # morning vs evening
            'group_dynamics': {},     # solo vs group activities
            'cuisine_preference': {}, # food choices
            'travel_style': {}        # packed vs relaxed
        }
    
    async def learn_from_decision(
        self,
        component: TripComponent,
        decision: ComponentDecision,
        context: TripContext
    ):
        if decision == ComponentDecision.CHOSEN:
            # Reinforce positive patterns
            self.reinforce_patterns(component.tags, positive=True)
            self.update_price_preference(component.price_range, positive=True)
            
        elif decision == ComponentDecision.VETOED:
            # Learn negative patterns
            self.reinforce_patterns(component.tags, positive=False)
            # Store specific veto reasons
            await self.store_veto_pattern(component, context)
            
        elif decision == ComponentDecision.CONSIDERING:
            # Track uncertainty patterns
            self.track_consideration_factors(component, context)
```

## Backup Activation System

```python
class BackupActivationManager:
    async def check_component_viability(
        self,
        component: TripComponent,
        date: datetime
    ) -> ComponentStatus:
        # Check multiple factors
        checks = await asyncio.gather(
            self.check_weather_impact(component, date),
            self.check_availability(component, date),
            self.check_timing_conflicts(component, date),
            self.check_special_conditions(component, date)
        )
        
        if any(check.requires_backup for check in checks):
            return ComponentStatus(
                viable=False,
                reason=checks[0].reason,
                suggested_backups=await self.get_relevant_backups(component)
            )
        
        return ComponentStatus(viable=True)
    
    async def activate_backup(
        self,
        primary: TripComponent,
        trip: Trip
    ) -> Optional[TripComponent]:
        # Get user's backup choices
        backups = await self.get_user_backups(primary, trip)
        
        # If no user backup, use AI suggestion
        if not backups:
            backups = await self.suggest_smart_backup(primary, trip)
        
        # Find first viable backup
        for backup in backups:
            if await self.check_component_viability(backup, trip.date):
                return backup
                
        return None
```

## Real-time Adaptation

```python
class ItineraryAdapter:
    async def adapt_to_conditions(
        self,
        itinerary: Itinerary,
        current_conditions: Dict
    ) -> AdaptedItinerary:
        adaptations = []
        
        for day in itinerary.days:
            for component in day.components:
                if component.decision == ComponentDecision.CHOSEN:
                    status = await self.check_real_time_viability(
                        component,
                        current_conditions
                    )
                    
                    if not status.viable:
                        # Try to activate backup
                        backup = await self.activate_backup(component, day)
                        if backup:
                            adaptations.append(
                                Adaptation(
                                    original=component,
                                    replacement=backup,
                                    reason=status.reason
                                )
                            )
                        else:
                            # Suggest new alternatives
                            alternatives = await self.find_emergency_alternatives(
                                component,
                                current_conditions
                            )
                            adaptations.append(
                                Adaptation(
                                    original=component,
                                    suggestions=alternatives,
                                    reason=status.reason
                                )
                            )
        
        return AdaptedItinerary(
            original=itinerary,
            adaptations=adaptations,
            conditions=current_conditions
        )
```

## Usage Example

```python
# User interaction flow
async def handle_component_decision(
    component_id: str,
    decision: ComponentDecision,
    reason: Optional[str]
):
    # 1. Record decision
    await db.record_component_decision(
        component_id=component_id,
        decision=decision,
        reason=reason
    )
    
    # 2. Learn from decision
    await learning_engine.learn_from_decision(
        component=component,
        decision=decision,
        context=trip_context
    )
    
    # 3. If vetoed, remove from future suggestions
    if decision == ComponentDecision.VETOED:
        await preference_manager.add_veto_pattern(component)
    
    # 4. If backup, map as alternative
    elif decision == ComponentDecision.BACKUP:
        await backup_manager.register_backup(component, trip)
    
    # 5. Update UI
    return {
        "status": "decision_recorded",
        "updated_itinerary": await get_updated_itinerary(trip_id),
        "swap_suggestions": await get_swap_suggestions(component_id) if requested
    }
```

## Benefits

1. **Personalization**: Learn from every decision to improve future recommendations
2. **Flexibility**: Easy swapping and backup options for maximum adaptability  
3. **Resilience**: Automatic adaptation to closures, weather, and other disruptions
4. **Memory**: Never suggest vetoed options again, remember what works
5. **Proactive**: Pre-identified backups ready when needed

This system ensures that users have full control over their itinerary while the AI learns and adapts to provide increasingly personalized suggestions.