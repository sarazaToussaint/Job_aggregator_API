from fastapi import FastAPI
from app.db import Base, engine
from app.routers import jobs, subscribers

app = FastAPI(title="Job Aggregator API")

# Include routers
app.include_router(jobs.router)
app.include_router(subscribers.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to Job Aggregator API! Visit /docs for API docs."}


@app.on_event("startup")
def startup():
    # Create tables at startup (non-blocking during import)
    Base.metadata.create_all(bind=engine)
