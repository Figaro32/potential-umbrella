from pydantic import BaseModel, ConfigDict, Field


class JobCreate(BaseModel):
    technician: str = Field(min_length=1)
    notes: str = Field(min_length=1)

class JobResponse(JobCreate):
    id: str
    status: str

    model_config = ConfigDict(from_attributes=True)