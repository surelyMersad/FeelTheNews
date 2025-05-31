from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from typing import Dict, Any

class SentimentService:
    def __init__(self):
        try:
            self.tokenizer = AutoTokenizer.from_pretrained("yiyanghkust/finbert-tone")
            self.model = AutoModelForSequenceClassification.from_pretrained("yiyanghkust/finbert-tone")
        except Exception as e:
            raise Exception(f"Error loading FinBERT model: {str(e)}")

    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment of text using FinBERT
        Returns sentiment label and confidence scores
        """
        if not text:
            return {
                "sentiment": "neutral",
                "confidence": 1.0,
                "scores": {
                    "positive": 0.0,
                    "neutral": 1.0,
                    "negative": 0.0
                }
            }

        # Tokenize and get sentiment
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        outputs = self.model(**inputs)
        predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
        
        # Get sentiment labels and scores
        sentiment_labels = ["positive", "neutral", "negative"]
        sentiment_scores = predictions[0].tolist()
        
        # Get the dominant sentiment
        dominant_sentiment = sentiment_labels[sentiment_scores.index(max(sentiment_scores))]
        
        return {
            "sentiment": dominant_sentiment,
            "confidence": max(sentiment_scores),
            "scores": dict(zip(sentiment_labels, sentiment_scores))
        } 