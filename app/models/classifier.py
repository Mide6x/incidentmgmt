from transformers import pipeline
from typing import Tuple
import torch

class IncidentClassifier:
    def __init__(self):
        self.classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli",
            device=-1  # Use CPU
        )
        
        # Updated categories based on TRACE's commodity trading context
        self.categories = [
            # Documentation & Compliance
            "Documentation Issue",        # Missing/incorrect trade documents
            "Compliance Violation",       # KYC/regulatory compliance issues
            "Contract Issue",            # Contract-related problems
            
            # Logistics & Shipment
            "Shipment Delay",            # Delays in transportation
            "Damaged Goods",             # Physical damage to goods
            "Quality Control",           # Product quality issues
            "Storage Issue",             # Warehouse/storage problems
            "Transportation Issue",       # Vehicle/carrier problems
            
            # Financial & Payment
            "Payment Issue",             # Payment delays or problems
            "Financing Problem",         # Issues with trade financing
            "Currency Risk",             # Exchange rate/currency issues
            
            # Technical & System
            "Platform Technical Issue",   # TRACE system technical problems
            "Integration Error",          # Issues with external system integration
            "Data Synchronization",       # Data consistency problems
            
            # Trade Operations
            "Aggregation Issue",         # Problems with commodity aggregation
            "Verification Failure",       # Buyer/seller verification issues
            "Trade Execution Error",      # Issues in trade execution
            
            # Communication & Support
            "Communication Breakdown",    # Issues in stakeholder communication
            "Stakeholder Dispute",        # Conflicts between parties
            
            # Supply Chain
            "Supply Shortage",           # Issues with commodity availability
            "Quality Assurance",         # Product quality control issues
            "Traceability Issue"         # Problems with product tracing
        ]

    def classify(self, title: str, description: str) -> Tuple[str, float]:
        # Combine title and description for better context
        text = f"{title} {description}"
        
        try:
            # Perform classification with more specific hypothesis template
            result = self.classifier(
                text,
                candidate_labels=self.categories,
                hypothesis_template="This trade incident involves {}."
            )
            
            # Convert logits to probabilities if needed
            if isinstance(result['scores'], torch.Tensor):
                scores = result['scores'].cpu().numpy().tolist()
            else:
                scores = result['scores']
                
            return result['labels'][0], scores[0]
            
        except Exception as e:
            # Fallback to default category if classification fails
            print(f"Classification error: {str(e)}")
            return "Platform Technical Issue", 0.5
