from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app import crud, schemas

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.post("/", response_model=schemas.JobRead)
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db)):
    return crud.jobs.create_job(db, job)


@router.get("/", response_model=list[schemas.JobRead])
def get_jobs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.jobs.get_jobs(db, skip, limit)
