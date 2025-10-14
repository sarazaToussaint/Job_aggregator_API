from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict
from datetime import datetime


class JobBase(BaseModel):
    title: str
    company: str
    location: Optional[str] = None
    url: str


# Schema for creating a job
class JobCreate(JobBase):
    pass


# Schema for reading a job (includes ID)
class Job(JobBase):
    id: int

    class Config:
        from_attributes = True


# --- SUBSCRIBER SCHEMAS ---

class SubscriberBase(BaseModel):
    email: EmailStr
    filters: Optional[Dict] = None


class SubscriberCreate(SubscriberBase):
    pass


class Subscriber(SubscriberBase):
    id: int
    verified: bool
    plan: str
    created_at: datetime

    class Config:
        from_attributes = True
