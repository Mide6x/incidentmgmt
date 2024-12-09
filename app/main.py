from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Body, Depends
from app.schemas.incident import IncidentInput, IncidentResponse, IncidentCreate
from app.schemas.combined_analysis import CombinedAnalysis, Entity
from app.models.classifier import IncidentClassifier
from app.models.entity_extractor import EntityExtractor
from app.models.sentiment_analyzer import SentimentAnalyzer
from app.models.recommender import IncidentRecommender
from app.utils.document_processor import DocumentProcessor
from typing import List, Optional
import os
import json
from datetime import datetime

app = FastAPI(title="AI Incident Management API")

# Initialize all analyzers
classifier = IncidentClassifier()
extractor = EntityExtractor()
sentiment_analyzer = SentimentAnalyzer()
recommender = IncidentRecommender()
doc_processor = DocumentProcessor(upload_dir="temp_uploads")

# In-memory storage for incidents
incidents = []
current_id = 1

@app.post("/incidents/create", response_model=IncidentResponse)
async def create_incident(
    title: str,
    description: str,
    documents: Optional[List[UploadFile]] = File(None)
):
    global current_id
    
    incident = IncidentInput(title=title, description=description)
    
    # First analyze the incident
    analysis = await analyze_incident(incident)
    
    # Process documents if any
    document_texts = []
    if documents:
        for doc in documents:
            file_path = await doc_processor.save_file(doc, current_id)
            extracted_text = doc_processor.extract_text(file_path)
            document_texts.append(extracted_text)
            # Clean up the file after extraction
            os.remove(file_path)
    
    # Create incident
    new_incident = {
        "id": current_id,
        "title": incident.title,
        "description": incident.description,
        "category": analysis.category,
        "urgency_level": analysis.urgency_level,
        "status": "open",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "document_count": len(documents) if documents else 0
    }
    
    incidents.append(new_incident)
    current_id += 1
    
    return new_incident

@app.post("/incidents/analyze", response_model=CombinedAnalysis)
async def analyze_incident(incident: IncidentInput):
    full_text = f"{incident.title} {incident.description}"
    
    # Get classification
    category, confidence = classifier.classify(incident.title, incident.description)
    
    # Get sentiment and urgency
    sentiment, urgency = sentiment_analyzer.analyze(full_text)
    
    # Extract entities
    entities = []
    try:
        extracted_entities = extractor.extract_entities(full_text)
        entities = [
            Entity(entity=e.entity, type=e.type)
            for e in extracted_entities
            if e.type in ["Tracking ID", "Product"]
        ]
    except Exception as e:
        print(f"Entity extraction error: {str(e)}")
    
    # Get recommendations
    recommendations, resolution_time = recommender.get_recommendations(
        category=category,
        description=full_text,
        urgency=urgency
    )
    
    return CombinedAnalysis(
        category=category,
        confidence=confidence,
        sentiment=sentiment,
        urgency_level=urgency,
        entities=entities if entities else None,
        recommended_actions=recommendations,
        estimated_resolution_time=resolution_time
    )

@app.get("/incidents/metrics")
async def get_metrics():
    try:
        total = len(incidents)
        high_priority = sum(1 for inc in incidents if inc["urgency_level"] == "High")
        open_incidents = sum(1 for inc in incidents if inc["status"] == "open")
        resolved = sum(1 for inc in incidents if inc["status"] == "resolved")
        
        return {
            "total_incidents": total,
            "high_priority": high_priority,
            "open": open_incidents,
            "resolved": resolved,
            "by_category": {
                category: sum(1 for inc in incidents if inc["category"] == category)
                for category in classifier.categories
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching metrics: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
