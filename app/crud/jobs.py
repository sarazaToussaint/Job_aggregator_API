from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from app import models, schemas
from typing import Optional, List
from datetime import datetime


def get_jobs(
    db: Session, 
    skip: int = 0, 
    limit: int = 10, 
    title: Optional[str] = None, 
    company: Optional[str] = None, 
    location: Optional[str] = None, 
    tags: Optional[List[str]] = None, 
    is_remote: Optional[bool] = None, 
    posted_after: Optional[datetime] = None, 
    posted_before: Optional[datetime] = None
):
    query = db.query(models.Job)
    if title:
        query = query.filter(models.Job.title.ilike(f"%{title}%"))
    if company:
        query = query.filter(models.Job.company.ilike(f"%{company}%"))
    if location:
        query = query.filter(models.Job.location.ilike(f"%{location}%"))
    if tags:
        for tag in tags:
            query = query.filter(models.Job.tags.contains([tag]))
    if is_remote is not None:
        query = query.filter(models.Job.is_remote == is_remote)
    if posted_after:
        query = query.filter(models.Job.posted_date >= posted_after)
    if posted_before:
        query = query.filter(models.Job.posted_date <= posted_before)
    return query.offset(skip).limit(limit).all()


def get_job_by_id(db: Session, job_id: int):
    return db.query(models.Job).filter(models.Job.id == job_id).first()


def get_job_by_url(db: Session, job_url: str):
    return db.query(models.Job).filter(models.Job.url == job_url).first()


def create_job(db: Session, job: schemas.JobCreate):
    db_job = models.Job(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


def update_job(db: Session, job_id: int, job_update: schemas.JobUpdate):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        return None
    update_data = job_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(job, key, value)
    db.commit()
    db.refresh(job)
    return job


def delete_job(db: Session, job_id: int):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        return False
    db.delete(job)
    db.commit()
    return True
