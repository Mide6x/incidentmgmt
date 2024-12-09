from typing import List, Optional
from pydantic import BaseModel

class Entity(BaseModel):
    entity: str
    type: str

class CombinedAnalysis(BaseModel):
    category: str
    confidence: float
    sentiment: str
    urgency_level: str
    entities: Optional[List[Entity]] = None
    recommended_actions: List[str]
    estimated_resolution_time: str 