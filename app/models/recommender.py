from typing import List, Tuple

class IncidentRecommender:
    def __init__(self):
        # Predefined resolution templates based on incident types
        self.resolution_templates = {
            # Quality & Standards
            "Damaged Goods": [
                "Initiate immediate damage assessment within 4 hours",
                "Document damage with photos and inspection report",
                "File insurance claim if damage exceeds threshold"
            ],
            "Quality Control": [
                "Schedule immediate quality inspection within 2 hours",
                "Collect samples for laboratory testing if required",
                "Prepare quality deviation report with findings"
            ],
            "Standards Violation": [
                "Review product specifications against standards",
                "Collect non-conformance evidence and documentation",
                "Schedule supplier quality audit within 24 hours"
            ],
            # Documentation & Compliance
            "Documentation Issue": [
                "Request missing documents from the responsible party within 4 hours",
                "Schedule document verification with compliance team within 24 hours",
                "Set up automated reminders for document submission every 8 hours"
            ],
            "Compliance Violation": [
                "Initiate immediate compliance review within 2 hours",
                "Prepare violation report and notify regulatory team",
                "Schedule stakeholder meeting to address compliance gaps"
            ],
            "Contract Issue": [
                "Review contract terms with legal team within 24 hours",
                "Prepare amendment documentation if required",
                "Schedule resolution meeting with counterparty"
            ],
            
            # Logistics & Shipment
            "Shipment Delay": [
                "Request immediate status update from logistics provider",
                "Calculate impact on delivery timeline and notify stakeholders",
                "Identify alternative routing options within 8 hours"
            ],
            "Transportation Issue": [
                "Arrange backup transportation within 6 hours",
                "Update tracking system with new vehicle details",
                "Schedule 4-hourly status updates from transport team"
            ],
            "Storage Issue": [
                "Assess current storage condition within 2 hours",
                "Identify alternative storage facilities if needed",
                "Monitor commodity condition every 6 hours"
            ],
            
            # Financial & Payment
            "Payment Issue": [
                "Contact treasury team for payment status within 2 hours",
                "Prepare payment reconciliation report",
                "Set up payment tracking checkpoints"
            ],
            "Financing Problem": [
                "Escalate to finance team for immediate review",
                "Prepare alternative financing options within 24 hours",
                "Schedule stakeholder update meeting"
            ],
            
            # Technical & System
            "Platform Technical Issue": [
                "Initiate system diagnostic within 1 hour",
                "Implement temporary workaround if available",
                "Schedule technical team review within 4 hours"
            ],
            "Integration Error": [
                "Check integration logs for error patterns",
                "Initiate failover to backup systems if available",
                "Schedule technical team intervention within 2 hours"
            ]
        }
         # Urgency calculation factors
        self.urgency_factors = {
            # High Priority Issues
            "Damaged Goods": "High",          # Physical damage requires immediate attention
            "Quality Control": "High",        # Quality issues need quick resolution
            "Payment Issue": "High",          # Financial impact needs rapid response
            "Shipment Delay": "High",         # Time-sensitive logistics issues
            "Transportation Issue": "High",    # Immediate logistics problems
            "Platform Technical Issue": "High",# System issues affecting operations
            "Supply Shortage": "High",        # Critical supply chain issues
            "Compliance Violation": "High",    # Regulatory risks need quick action
            
            # Medium Priority Issues
            "Documentation Issue": "Medium",   # Administrative but important
            "Storage Issue": "Medium",        # Facility management issues
            "Integration Error": "Medium",     # Technical but not critical
            "Data Synchronization": "Medium", # System reconciliation issues
            "Communication Breakdown": "Medium", # Stakeholder management
            "Quality Assurance": "Medium",    # Preventive quality measures
            "Verification Failure": "Medium", # Process validation issues
            
            # Lower Priority Issues
            "Contract Issue": "Low",          # Requires thorough review
            "Currency Risk": "Low",           # Long-term financial planning
            "Traceability Issue": "Low",      # Documentation and tracking
            "Aggregation Issue": "Low",       # Data consolidation
            "Trade Execution Error": "Low",   # Process improvements
            
            # Default for any uncategorized issues
            "default": "Medium"
        }
        
        # Impact keywords for urgency calculation
        self.high_impact_keywords = [
            "immediate", "urgent", "critical", "severe", "damaged",
            "breach", "violation", "failed", "emergency", "risk"
        ]
        # SLA breach times based on urgency (in hours)
        self.sla_times = {
            "High": 24,    # 1 day
            "Medium": 48,  # 2 days
            "Low": 72     # 3 days
        }

    def get_recommendations(self, category: str, description: str, urgency: str) -> Tuple[List[str], str]:
        # Calculate urgency based on description and category
        calculated_urgency = self._calculate_urgency(category, description)
        
        # Get predefined actions for the category
        actions = self.resolution_templates.get(
            category, 
            [
                "Escalate to relevant department for immediate review",
                "Schedule stakeholder update within 24 hours",
                "Document incident details and track resolution progress"
            ]
        )
        
        # Calculate resolution time based on calculated urgency and SLA
        resolution_hours = min(
            self.sla_times[calculated_urgency],
            self._calculate_resolution_time(category, calculated_urgency)
        )
        
        return actions, f"{resolution_hours} hours"
    
    def _calculate_resolution_time(self, category: str, urgency: str) -> int:
        # Base resolution times (in hours) for different categories
        base_times = {
            "Documentation Issue": 24,
            "Compliance Violation": 48,
            "Transportation Issue": 12,
            "Shipment Delay": 24,
            "Payment Issue": 24,
            "Platform Technical Issue": 8,
            "Integration Error": 12
        }
        
        # Get base time or default to 24 hours
        base_time = base_times.get(category, 24)
        
        # Adjust based on urgency
        urgency_multiplier = {
            "High": 0.7,    # Reduce time for high urgency
            "Medium": 1.0,  # Standard time
            "Low": 1.5      # Allow more time for low urgency
        }
        
        estimated_hours = int(base_time * urgency_multiplier[urgency])
        
        # Ensure within SLA limits
        return min(estimated_hours, self.sla_times[urgency])
    
    def _calculate_urgency(self, category: str, description: str) -> str:
        # Base urgency from category
        base_urgency = self.urgency_factors.get(category, "Medium")
        
        # Count impact keywords in description
        impact_words = sum(1 for word in self.high_impact_keywords 
                         if word in description.lower())
        
        # Adjust urgency based on keywords
        if impact_words >= 2:
            return "High"
        elif impact_words == 1 and base_urgency != "Low":
            return "High"
        elif impact_words == 0 and base_urgency == "High":
            return "Medium"
            
        return base_urgency