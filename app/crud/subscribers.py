from sqlalchemy.orm import Session
from app import models, schemas


def get_subscribers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Subscriber).offset(skip).limit(limit).all()


def create_subscriber(db: Session, subscriber: schemas.SubscriberCreate):
    db_subscriber = models.Subscriber(**subscriber.model_dump())
    db.add(db_subscriber)
    db.commit()
    db.refresh(db_subscriber)
    return db_subscriber


def update_subscriber(db: Session, subscriber_id: int, subscriber_update: schemas.SubscriberUpdate):
    subscriber = db.query(models.Subscriber).filter(models.Subscriber.id == subscriber_id).first()
    if not subscriber:
        return None
    update_data = subscriber_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(subscriber, key, value)
    db.commit()
    db.refresh(subscriber)
    return subscriber


def delete_subscriber(db: Session, subscriber_id: int):
    subscriber = db.query(models.Subscriber).filter(models.Subscriber.id == subscriber_id).first()
    if not subscriber:
        return False
    db.delete(subscriber)
    db.commit()
    return True