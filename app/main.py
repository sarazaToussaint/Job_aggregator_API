from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app import models, schemas, crud

app = FastAPI(title="Job Aggregator API")


# ✅ Root route (for testing)
@app.get("/")
def root():
    return {"message": "Welcome to the Job Aggregator API"}


# ✅ Get all jobs
@app.get("/jobs")
def get_jobs(db: Session = Depends(get_db)):
    jobs = crud.get_jobs(db)
    return jobs


# ✅ Create a new job
@app.post("/jobs")
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db)):
    return crud.create_job(db, job)


# ✅ Get all suscribers
@app.get("/subscribers", response_model=list[schemas.Subscriber])
def read_subscribers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_subscribers(db, skip=skip, limit=limit)


# ✅ Create a new subscriber
@app.post("/subscribers", response_model=schemas.Subscriber)
def create_subscriber(subscriber: schemas.SubscriberCreate, db: Session = Depends(get_db)):
    return crud.create_subscriber(db=db, subscriber=subscriber)
