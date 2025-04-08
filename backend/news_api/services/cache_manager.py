from django.core.cache import cache
from django.conf import settings
import json
from typing import Any, Optional
import logging

logger = logging.getLogger(__name__)

class CacheManager:
    def __init__(self):
        self.default_timeout = 600  # 10 minutes default cache timeout
    
    def get_cached_articles(self, cache_key: str) -> Optional[list]:
        """
        Get cached articles
        
        Args:
            cache_key (str): Cache key for articles
            
        Returns:
            Optional[list]: Cached articles or None if not found
        """
        try:
            cached_data = cache.get(cache_key)
            if cached_data:
                return json.loads(cached_data)
            return None
        except Exception as e:
            logger.error(f"Error getting cached articles: {str(e)}")
            return None
    
    def set_cached_articles(self, cache_key: str, articles: list, timeout: int = None) -> bool:
        """
        Cache articles
        
        Args:
            cache_key (str): Cache key for articles
            articles (list): List of articles to cache
            timeout (int, optional): Cache timeout in seconds
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            timeout = timeout or self.default_timeout
            cache.set(
                cache_key,
                json.dumps(articles, default=str),
                timeout
            )
            return True
        except Exception as e:
            logger.error(f"Error caching articles: {str(e)}")
            return False
    
    def get_cached_sentiment(self, article_id: int) -> Optional[dict]:
        """
        Get cached sentiment analysis
        
        Args:
            article_id (int): Article ID
            
        Returns:
            Optional[dict]: Cached sentiment analysis or None if not found
        """
        try:
            cache_key = f"sentiment_{article_id}"
            cached_data = cache.get(cache_key)
            if cached_data:
                return json.loads(cached_data)
            return None
        except Exception as e:
            logger.error(f"Error getting cached sentiment: {str(e)}")
            return None
    
    def set_cached_sentiment(self, article_id: int, sentiment_data: dict, timeout: int = None) -> bool:
        """
        Cache sentiment analysis
        
        Args:
            article_id (int): Article ID
            sentiment_data (dict): Sentiment analysis data
            timeout (int, optional): Cache timeout in seconds
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            timeout = timeout or self.default_timeout
            cache_key = f"sentiment_{article_id}"
            cache.set(
                cache_key,
                json.dumps(sentiment_data),
                timeout
            )
            return True
        except Exception as e:
            logger.error(f"Error caching sentiment: {str(e)}")
            return False
    
    def invalidate_cache(self, pattern: str) -> bool:
        """
        Invalidate cache by pattern
        
        Args:
            pattern (str): Cache key pattern to invalidate
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            keys = cache.keys(pattern)
            for key in keys:
                cache.delete(key)
            return True
        except Exception as e:
            logger.error(f"Error invalidating cache: {str(e)}")
            return False 