from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    def __init__(self):
        self.model_name = "ProsusAI/finbert"
        self.tokenizer = None
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load the FinBERT model and tokenizer"""
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
    
    def analyze(self, text: str) -> Tuple[str, float]:
        """
        Analyze the sentiment of the given text
        
        Args:
            text (str): The text to analyze
            
        Returns:
            Tuple[str, float]: (sentiment, confidence_score)
        """
        try:
            inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
            outputs = self.model(**inputs)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
            
            # Get the predicted class and confidence
            predicted_class = torch.argmax(predictions).item()
            confidence = predictions[0][predicted_class].item()
            
            # Map the class index to sentiment
            sentiment_map = {0: 'positive', 1: 'negative', 2: 'neutral'}
            sentiment = sentiment_map[predicted_class]
            
            return sentiment, confidence
            
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {str(e)}")
            raise
    
    def analyze_batch(self, texts: list) -> list:
        """
        Analyze sentiment for a batch of texts
        
        Args:
            texts (list): List of texts to analyze
            
        Returns:
            list: List of (sentiment, confidence) tuples
        """
        return [self.analyze(text) for text in texts] 