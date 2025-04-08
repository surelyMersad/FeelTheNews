import requests
from datetime import datetime, timedelta
import logging
from typing import List, Dict
from django.conf import settings
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class NewsFetcher:
    def __init__(self):
        self.api_key = os.getenv('NYT_API_KEY')
        self.base_url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
        
        if not self.api_key:
            raise ValueError("NYT_API_KEY environment variable is not set")
    
    def fetch_articles(self, 
                      query: str = None,
                      start_date: datetime = None,
                      end_date: datetime = None,
                      page: int = 1) -> List[Dict]:
        """
        Fetch articles from NYT API
        
        Args:
            query (str, optional): Search query
            start_date (datetime, optional): Start date for articles
            end_date (datetime, optional): End date for articles
            page (int, optional): Page number for pagination
            
        Returns:
            List[Dict]: List of article dictionaries
        """
        try:
            params = {
                'api-key': self.api_key,
                'page': page,
                'sort': 'newest'
            }
            
            if query:
                params['q'] = query
            if start_date:
                params['begin_date'] = start_date.strftime('%Y%m%d')
            if end_date:
                params['end_date'] = end_date.strftime('%Y%m%d')
            
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            articles = []
            
            for article in data.get('response', {}).get('docs', []):
                articles.append({
                    'title': article.get('headline', {}).get('main'),
                    'content': article.get('abstract'),
                    'url': article.get('web_url'),
                    'published_date': datetime.strptime(
                        article.get('pub_date', '').split('T')[0],
                        '%Y-%m-%d'
                    ),
                    'source': 'New York Times'
                })
            
            return articles
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching articles: {str(e)}")
            raise
    
    def fetch_latest_articles(self, hours: int = 24) -> List[Dict]:
        """
        Fetch latest articles from the last N hours
        
        Args:
            hours (int): Number of hours to look back
            
        Returns:
            List[Dict]: List of article dictionaries
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(hours=hours)
        return self.fetch_articles(start_date=start_date, end_date=end_date) 