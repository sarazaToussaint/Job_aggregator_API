from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app import crud, schemas

router = APIRouter(prefix="/subscribers", tags=["Subscribers"])


@router.post("/", response_model=schemas.SubscriberRead)
def create_subscriber(subscriber: schemas.SubscriberCreate, db: Session = Depends(get_db)):
    return crud.subscribers.create_subscriber(db, subscriber)


@router.get("/", response_model=list[schemas.SubscriberRead])
def get_subscribers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.subscribers.get_subscribers(db, skip, limit)
