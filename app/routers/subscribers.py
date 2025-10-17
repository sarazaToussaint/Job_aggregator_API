from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
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

@router.put("/{subscriber_id}", response_model=schemas.SubscriberRead)
def update_subscriber(subscriber_id: int, subscriber_update: schemas.SubscriberUpdate, db: Session = Depends(get_db)):
    subscriber = crud.subscribers.update_subscriber(db, subscriber_id, subscriber_update)
    if not subscriber:
        raise HTTPException(status_code=404, detail="Subscriber not found")
    return subscriber

@router.delete("/{subscriber_id}")
def delete_subscriber(subscriber_id: int, db: Session = Depends(get_db)):
    result = crud.subscribers.delete_subscriber(db, subscriber_id)
    if not result:
        raise HTTPException(status_code=404, detail="Subscriber not found")
    return {"message": "Subscriber deleted successfully"}    
