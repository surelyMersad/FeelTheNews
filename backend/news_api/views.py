from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Article, SentimentAnalysis
from .services.sentiment_analyzer import SentimentAnalyzer
from .services.news_fetcher import NewsFetcher
from .services.cache_manager import CacheManager
import logging

logger = logging.getLogger(__name__)

class NewsViewSet(viewsets.ViewSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.news_fetcher = NewsFetcher()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.cache_manager = CacheManager()
    
    @action(detail=False, methods=['get'])
    def latest(self, request):
        """Get latest news articles with sentiment analysis"""
        try:
            # Check cache first
            cache_key = 'latest_articles'
            cached_articles = self.cache_manager.get_cached_articles(cache_key)
            
            if cached_articles:
                return Response(cached_articles)
            
            # Fetch new articles
            articles = self.news_fetcher.fetch_latest_articles(hours=24)
            
            # Analyze sentiment for each article
            for article in articles:
                sentiment, confidence = self.sentiment_analyzer.analyze(article['title'])
                article['sentiment'] = sentiment
                article['confidence'] = confidence
            
            # Cache the results
            self.cache_manager.set_cached_articles(cache_key, articles)
            
            return Response(articles)
            
        except Exception as e:
            logger.error(f"Error fetching latest articles: {str(e)}")
            return Response(
                {'error': 'Failed to fetch latest articles'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search articles with optional date filtering"""
        try:
            query = request.query_params.get('q', '')
            start_date = request.query_params.get('start_date')
            end_date = request.query_params.get('end_date')
            
            # Create cache key based on search parameters
            cache_key = f"search_{query}_{start_date}_{end_date}"
            
            # Check cache first
            cached_results = self.cache_manager.get_cached_articles(cache_key)
            if cached_results:
                return Response(cached_results)
            
            # Parse dates if provided
            if start_date:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
            if end_date:
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
            
            # Fetch articles
            articles = self.news_fetcher.fetch_articles(
                query=query,
                start_date=start_date,
                end_date=end_date
            )
            
            # Analyze sentiment for each article
            for article in articles:
                sentiment, confidence = self.sentiment_analyzer.analyze(article['title'])
                article['sentiment'] = sentiment
                article['confidence'] = confidence
            
            # Cache the results
            self.cache_manager.set_cached_articles(cache_key, articles)
            
            return Response(articles)
            
        except Exception as e:
            logger.error(f"Error searching articles: {str(e)}")
            return Response(
                {'error': 'Failed to search articles'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'])
    def refresh(self, request):
        """Force refresh of latest articles"""
        try:
            # Invalidate cache
            self.cache_manager.invalidate_cache('latest_articles')
            
            # Fetch new articles
            articles = self.news_fetcher.fetch_latest_articles(hours=24)
            
            # Analyze sentiment for each article
            for article in articles:
                sentiment, confidence = self.sentiment_analyzer.analyze(article['title'])
                article['sentiment'] = sentiment
                article['confidence'] = confidence
            
            # Cache the new results
            self.cache_manager.set_cached_articles('latest_articles', articles)
            
            return Response(articles)
            
        except Exception as e:
            logger.error(f"Error refreshing articles: {str(e)}")
            return Response(
                {'error': 'Failed to refresh articles'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) 