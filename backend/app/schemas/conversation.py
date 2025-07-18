from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field

from app.models.conversation import ConversationState, MessageRole


class MessageBase(BaseModel):
    content: str
    role: MessageRole


class MessageCreate(MessageBase):
    pass


class Message(MessageBase):
    id: UUID
    conversation_id: UUID
    created_at: datetime
    llm_metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        from_attributes = True


class ConversationBase(BaseModel):
    state: ConversationState = ConversationState.INITIAL_INTENT
    context: Dict[str, Any] = Field(default_factory=dict)


class ConversationCreate(ConversationBase):
    trip_id: Optional[UUID] = None


class ConversationUpdate(BaseModel):
    state: Optional[ConversationState] = None
    context: Optional[Dict[str, Any]] = None
    trip_id: Optional[UUID] = None


class Conversation(ConversationBase):
    id: UUID
    user_id: UUID
    trip_id: Optional[UUID]
    created_at: datetime
    updated_at: datetime
    messages: List[Message] = []
    
    class Config:
        from_attributes = True


class ConversationWithMessages(Conversation):
    messages: List[Message]


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[UUID] = None


class ChatResponse(BaseModel):
    conversation_id: UUID
    message: Message
    state: ConversationState
    context: Dict[str, Any]