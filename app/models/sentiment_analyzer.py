from transformers import pipeline
from typing import Tuple

class SentimentAnalyzer:
    def __init__(self):
        self.analyzer = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
            device=-1  # Use CPU
        )
        
        # Urgency mapping based on sentiment scores
        self.urgency_levels = {
            (0.0, 0.3): "Low",
            (0.3, 0.6): "Medium",
            (0.6, 1.0): "High"
        }

    def analyze(self, text: str) -> Tuple[str, str]:
        result = self.analyzer(text)[0]
        score = result['score']
        
        # Map sentiment labels
        sentiment = "Negative" if result['label'] == "NEGATIVE" else "Positive"
        
        # Determine urgency level
        urgency = "Medium"  # default
        for (lower, upper), level in self.urgency_levels.items():
            if lower <= score <= upper:
                urgency = level
                break
                
        return sentiment, urgency 