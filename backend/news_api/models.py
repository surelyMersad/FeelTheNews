from django.db import models
from django.utils import timezone

class Article(models.Model):
    title = models.CharField(max_length=500)
    content = models.TextField()
    url = models.URLField(unique=True)
    published_date = models.DateTimeField()
    source = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.title

class SentimentAnalysis(models.Model):
    SENTIMENT_CHOICES = [
        ('positive', 'Positive'),
        ('neutral', 'Neutral'),
        ('negative', 'Negative'),
    ]
    
    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name='sentiment')
    sentiment = models.CharField(max_length=10, choices=SENTIMENT_CHOICES)
    confidence_score = models.FloatField()
    analyzed_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.article.title} - {self.sentiment}" 