from datetime import datetime
from uuid import uuid4
from enum import Enum

from sqlalchemy import Column, DateTime, ForeignKey, Text, JSON, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.user import Base


class ConversationState(str, Enum):
    INITIAL_INTENT = "initial_intent"
    GATHERING_CONTEXT = "gathering_context"
    REFINING_PREFERENCES = "refining_preferences"
    PRESENTING_OPTIONS = "presenting_options"
    DEEP_PLANNING = "deep_planning"
    BOOKING_ASSISTANCE = "booking_assistance"


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    trip_id = Column(UUID(as_uuid=True), ForeignKey("trips.id"), nullable=True)

    state = Column(
        SQLEnum(ConversationState),
        default=ConversationState.INITIAL_INTENT,
        nullable=False,
    )
    context = Column(JSON, default=dict)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="conversations")
    trip = relationship("Trip", back_populates="conversations")
    messages = relationship(
        "Message", back_populates="conversation", order_by="Message.created_at"
    )

    def __repr__(self):
        return f"<Conversation {self.id} - State: {self.state}>"


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    conversation_id = Column(
        UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False
    )

    role = Column(SQLEnum(MessageRole), nullable=False)
    content = Column(Text, nullable=False)

    # For storing LLM metadata (tokens used, model, etc.)
    llm_metadata = Column(JSON, default=dict)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    conversation = relationship("Conversation", back_populates="messages")

    def __repr__(self):
        return f"<Message {self.id} - {self.role}: {self.content[:50]}...>"
