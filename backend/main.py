from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from uuid import uuid4

app = FastAPI(title="FieldOps AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class JobCreate(BaseModel):
    technician: str
    notes: str = Field(min_length=1)

class Job(JobCreate):
    id: str
    status: str = "pending"

jobs : dict[str, Job] = {}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/jobs", response_model=Job, status_code=201)
def create_job(job: JobCreate):
    