# app/models.py
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Text,
    JSON,
    func,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    company = Column(String, index=True)
    location = Column(String, index=True)
    url = Column(String, unique=True, index=True)
    description = Column(Text)
    posted_date = Column(DateTime, nullable=True)
    source = Column(String)
    scraped_at = Column(DateTime, server_default=func.now())
    dedup_hash = Column(String, index=True)
    tags = Column(JSON, nullable=True)
    is_remote = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(),
                        onupdate=func.now())


class Subscriber(Base):
    __tablename__ = "subscribers"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    filters = Column(JSON, nullable=True)
    verified = Column(Boolean, default=False)
    verification_token = Column(String, nullable=True)
    plan = Column(String, default="free")
    created_at = Column(DateTime, server_default=func.now())
    last_sent_at = Column(DateTime, nullable=True)
    unsubscribed = Column(Boolean, default=False)
    updated_at = Column(DateTime, server_default=func.now(),
                        onupdate=func.now())
