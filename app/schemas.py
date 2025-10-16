# app/schemas.py

from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict
from datetime import datetime


class JobBase(BaseModel):
    title: str
    company: str
    location: Optional[str] = None
    url: str


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
