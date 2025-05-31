import os
import httpx
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

class NYTService:
    def __init__(self):
        self.api_key = os.getenv("NYT_API_KEY")
        if not self.api_key:
            raise ValueError("NYT API key not found in environment variables")
        
        self.base_url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"

    async def fetch_articles(self, keywords: List[str], begin_date: Optional[str] = None) -> List[dict]:
        """
        Fetch articles from NYT API based on keywords and optional date filter
        """
        # Construct query
        query = " OR ".join(keywords)
        
        # Prepare API request parameters
        params = {
            "api-key": self.api_key,
            "q": query,
            "sort": "newest"
        }
        
        if begin_date:
            params["begin_date"] = begin_date.replace("-", "")
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(self.base_url, params=params)
                response.raise_for_status()
                data = response.json()
                
                articles = []
                for article in data.get("response", {}).get("docs", []):
                    article_data = {
                        "title": article.get("headline", {}).get("main", ""),
                        "abstract": article.get("abstract", ""),
                        "url": article.get("web_url", ""),
                        "published_date": article.get("pub_date", "")
                    }
                    articles.append(article_data)
                
                return articles
                
            except httpx.HTTPError as e:
                raise Exception(f"Error fetching news from NYT API: {str(e)}") 