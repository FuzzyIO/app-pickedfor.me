from datetime import datetime
from uuid import uuid4
from enum import Enum

from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
    Date,
    Integer,
    Numeric,
    JSON,
    Enum as SQLEnum,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.user import Base


class TripStatus(str, Enum):
    PLANNING = "planning"
    BOOKED = "booked"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Trip(Base):
    __tablename__ = "trips"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    title = Column(String, nullable=True)
    status = Column(SQLEnum(TripStatus), default=TripStatus.PLANNING, nullable=False)

    # Trip details
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    destination = Column(String, nullable=True)

    # Party information
    party_size = Column(Integer, default=1)
    party_composition = Column(JSON, default=dict)  # e.g., {"adults": 2, "children": 1}

    # Budget
    budget_min = Column(Numeric, nullable=True)
    budget_max = Column(Numeric, nullable=True)
    budget_currency = Column(String, default="USD")

    # Preferences and context
    preferences = Column(JSON, default=dict)
    itinerary = Column(JSON, default=dict)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="trips")
    conversations = relationship("Conversation", back_populates="trip")

    def __repr__(self):
        return f"<Trip {self.id} - {self.title or 'Untitled'} ({self.status})>"
