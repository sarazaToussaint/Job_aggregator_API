from fastapi import APIRouter, Depends, HTTPException
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

@router.put("/{job_id}", response_model=schemas.JobRead)
def update_job(job_id: int, job_update: schemas.JobUpdate, db: Session = Depends(get_db)):
    job = crud.jobs.update_job(db, job_id, job_update)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job    

@router.delete("/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    result = crud.jobs.delete_job(db, job_id)
    if not result:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"message": "Job deleted successfully"}        