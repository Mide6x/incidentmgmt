import spacy
from typing import List
from app.schemas.entity import Entity

class EntityExtractor:
    def __init__(self):
        # Load English language model
        self.nlp = spacy.load("en_core_web_sm")
        
        # Add custom patterns for trade-specific entities
        ruler = self.nlp.add_pipe("entity_ruler", before="ner")
        patterns = [
            # Shipment ID patterns
            {"label": "TRACKING_ID", "pattern": [{"SHAPE": "ddd###"}]},
            {"label": "TRACKING_ID", "pattern": [{"SHAPE": "ddd####"}]},
            {"label": "TRACKING_ID", "pattern": [{"SHAPE": "###ddd"}]},
            
            # Document patterns
            {"label": "DOCUMENT", "pattern": "Bill of Lading"},
            {"label": "DOCUMENT", "pattern": "Certificate of Origin"},
            {"label": "DOCUMENT", "pattern": "customs forms"},
            {"label": "DOCUMENT", "pattern": "import license"},
            
            # Product patterns
            {"label": "PRODUCT", "pattern": [{"POS": "NOUN"}, {"LOWER": "shipment"}]},
            {"label": "PRODUCT", "pattern": [{"POS": "NOUN"}, {"LOWER": "cargo"}]},
            
            # Custom status patterns
            {"label": "STATUS", "pattern": "delayed"},
            {"label": "STATUS", "pattern": "pending"},
            {"label": "STATUS", "pattern": "cleared"},
            {"label": "STATUS", "pattern": "held"},
        ]
        ruler.add_patterns(patterns)

    def extract_entities(self, text: str) -> List[Entity]:
        # Process the text
        doc = self.nlp(text)
        
        entities = []
        for ent in doc.ents:
            # Map spaCy entity types to custom types
            entity_type = self._map_entity_type(ent.label_)
            
            # Create entity with confidence score
            entity = Entity(
                entity=ent.text,
                type=entity_type,
                start=ent.start_char,
                end=ent.end_char,
                confidence=self._calculate_confidence(ent)
            )
            entities.append(entity)
        
        return entities

    def _map_entity_type(self, spacy_label: str) -> str:
        """Map spaCy entity labels to custom labels"""
        mapping = {
            "TRACKING_ID": "Tracking ID",
            "DOCUMENT": "Document",
            "PRODUCT": "Product",
            "STATUS": "Status",
            "GPE": "Location",
            "ORG": "Organization",
            "DATE": "Date",
            "MONEY": "Amount",
        }
        return mapping.get(spacy_label, spacy_label)

    def _calculate_confidence(self, entity) -> float:
        """Calculate confidence score for entity"""
        # This is a simplified confidence calculation
        # In a production system, you'd want to use more sophisticated methods
        base_confidence = 0.8  # Base confidence for matched entities
        
        # Adjust confidence based on entity type and pattern match
        if entity.label_ in ["TRACKING_ID", "DOCUMENT"]:
            return base_confidence + 0.15
        elif entity.label_ in ["GPE", "DATE"]:
            return base_confidence + 0.1
        
        return base_confidence 