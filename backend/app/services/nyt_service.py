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
        # Format keywords for exact phrase matching
        formatted_keywords = [f'"{keyword}"' for keyword in keywords]
        query = " OR ".join(formatted_keywords)
        
        # Prepare API request parameters
        params = {
            "api-key": self.api_key,
            "q": query,
            "sort": "newest",
            "fl": "headline,abstract,web_url,pub_date,section_name,subsection_name"  # Fields we want to retrieve
        }
        
        if begin_date:
            # Convert YYYY-MM-DD to YYYYMMDD format
            params["begin_date"] = begin_date.replace("-", "")
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(self.base_url, params=params)
                response.raise_for_status()
                data = response.json()
                
                articles = []
                for article in data.get("response", {}).get("docs", []):
                    # Extract the main headline
                    headline = article.get("headline", {}).get("main", "")
                    
                    # Skip articles without a headline
                    if not headline:
                        continue
                    
                    article_data = {
                        "title": headline,
                        "abstract": article.get("abstract", ""),
                        "url": article.get("web_url", ""),
                        "published_date": article.get("pub_date", ""),
                        "section": article.get("section_name", ""),
                        "subsection": article.get("subsection_name", "")
                    }
                    articles.append(article_data)
                
                return articles
                
            except httpx.HTTPError as e:
                error_msg = f"Error fetching news from NYT API: {str(e)}"
                if e.response is not None:
                    error_msg += f" - Status: {e.response.status_code}"
                    try:
                        error_data = e.response.json()
                        if "fault" in error_data:
                            error_msg += f" - {error_data['fault']['faultstring']}"
                    except:
                        pass
                raise Exception(error_msg) 