from pydantic import BaseModel
from typing import List

class EntityInput(BaseModel):
    text: str

class Entity(BaseModel):
    entity: str
    type: str
    start: int
    end: int
    confidence: float

class EntityExtraction(BaseModel):
    entities: List[Entity] 