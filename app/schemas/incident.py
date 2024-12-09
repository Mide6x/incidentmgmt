from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from fastapi import UploadFile

class IncidentInput(BaseModel):
    title: str
    description: str

class IncidentCreate(BaseModel):
    title: str
    description: str
    documents: Optional[List[UploadFile]] = None

class IncidentResponse(BaseModel):
    id: int
    title: str
    description: str
    category: str
    urgency_level: str
    status: str
    created_at: datetime
    updated_at: datetime
    document_count: int
