from sqlalchemy.orm import Session
from app import models, schemas


def get_jobs(db: Session):
    return db.query(models.Job).all()


def create_job(db: Session, job: schemas.JobCreate):
    db_job = models.Job(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


# --- SUBSCRIBERS ---

def get_subscribers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Subscriber).offset(skip).limit(limit).all()


def create_subscriber(db: Session, subscriber: schemas.SubscriberCreate):
    db_subscriber = models.Subscriber(**subscriber.model_dump())
    db.add(db_subscriber)
    db.commit()
    db.refresh(db_subscriber)
    return db_subscriber
