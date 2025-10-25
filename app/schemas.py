from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict
from datetime import datetime


class JobBase(BaseModel):
    title: str
    company: str
    location: Optional[str] = None
    url: str
    description: Optional[str] = None
    posted_date: Optional[datetime] = None
    source: Optional[str] = None
    tags: Optional[list[str]] = None
    is_remote: Optional[bool] = None


class JobCreate(JobBase):
    pass


class JobRead(JobBase):
    id: int

    class Config:
        from_attributes = True


# --- SUBSCRIBER SCHEMAS ---

class SubscriberBase(BaseModel):
    email: EmailStr
    filters: Optional[Dict] = None


class SubscriberCreate(SubscriberBase):
    pass


class SubscriberRead(SubscriberBase):
    id: int
    verified: bool
    plan: str
    created_at: datetime

    class Config:
        from_attributes = True


class JobUpdate(BaseModel):
    """Fields to update an existing job. All optional."""
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    url: Optional[str] = None
    # Add other fields as desired for editing (e.g., description, tags, etc.)


class SubscriberUpdate(BaseModel):
    """Fields to update an existing subscriber. All optional."""
    email: Optional[EmailStr] = None
    filters: Optional[Dict] = None
    # Add other fields as desired (e.g., plan, verified)
