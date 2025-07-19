from datetime import datetime, date
from typing import Optional, Dict, Any
from uuid import UUID
from decimal import Decimal

from pydantic import BaseModel, Field

from app.models.trip import TripStatus


class TripBase(BaseModel):
    title: Optional[str] = None
    status: TripStatus = TripStatus.PLANNING
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    destination: Optional[str] = None
    party_size: int = 1
    party_composition: Dict[str, int] = Field(default_factory=dict)
    budget_min: Optional[Decimal] = None
    budget_max: Optional[Decimal] = None
    budget_currency: str = "USD"
    preferences: Dict[str, Any] = Field(default_factory=dict)
    itinerary: Dict[str, Any] = Field(default_factory=dict)


class TripCreate(TripBase):
    pass


class TripUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[TripStatus] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    destination: Optional[str] = None
    party_size: Optional[int] = None
    party_composition: Optional[Dict[str, int]] = None
    budget_min: Optional[Decimal] = None
    budget_max: Optional[Decimal] = None
    budget_currency: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None
    itinerary: Optional[Dict[str, Any]] = None


class Trip(TripBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
