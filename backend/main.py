from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from uuid import uuid4

from contextlib import asynccontextmanager

from sqlalchemy import select
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Job
from schemas import JobCreate, JobResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="FieldOps AI",
    lifespan = lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post(
    "/jobs", 
    response_model=JobResponse, 
    status_code=201
)
def create_job(
    data: JobCreate,
    db: Session = Depends(get_db)
):
    
    job = Job(
        id=str(uuid4()),
        technician=data.technician,
        notes=data.notes,
        status="pending"
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job

@app.get("/jobs", response_model=list[JobResponse])
def list_jobs(db: Session = Depends(get_db)):
    return db.scalars(select(Job)).all

@app.get(
    "/jobs/{job_id}", 
    response_model=JobResponse
)
def get_job(
    job_id: str,
    db: Session= Depends(get_db)
):
    job = db.get(Job, job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return job


