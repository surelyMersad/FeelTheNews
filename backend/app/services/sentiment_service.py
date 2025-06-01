from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class SentimentService:
    def __init__(self):
        try:
            logger.info("Initializing FinBERT model...")
            self.tokenizer = AutoTokenizer.from_pretrained("yiyanghkust/finbert-tone")
            self.model = AutoModelForSequenceClassification.from_pretrained("yiyanghkust/finbert-tone")
            logger.info("FinBERT model initialized successfully")
        except Exception as e:
            logger.error(f"Error loading FinBERT model: {str(e)}")
            raise Exception(f"Error loading FinBERT model: {str(e)}")

    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment of text using FinBERT
        Returns sentiment label and confidence scores
        """
        try:
            if not text or not isinstance(text, str):
                logger.warning("Empty or invalid text provided for sentiment analysis")
                return self._get_default_sentiment()

            # Clean and prepare text
            text = text.strip()
            if not text:
                return self._get_default_sentiment()

            # Tokenize and get sentiment
            inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
            with torch.no_grad():
                outputs = self.model(**inputs)
                predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
            
            # Get sentiment labels and scores
            sentiment_labels = ["positive", "neutral", "negative"]
            sentiment_scores = predictions[0].tolist()
            
            # Get the dominant sentiment
            max_score = max(sentiment_scores)
            dominant_sentiment = sentiment_labels[sentiment_scores.index(max_score)]
            
            return {
                "sentiment": dominant_sentiment,
                "confidence": float(max_score),
                "scores": {
                    label: float(score) for label, score in zip(sentiment_labels, sentiment_scores)
                }
            }
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {str(e)}")
            return self._get_default_sentiment()

    def _get_default_sentiment(self) -> Dict[str, Any]:
        """Return default neutral sentiment when analysis fails"""
        return {
            "sentiment": "neutral",
            "confidence": 1.0,
            "scores": {
                "positive": 0.0,
                "neutral": 1.0,
                "negative": 0.0
            }
        } 