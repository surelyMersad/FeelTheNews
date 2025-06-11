from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from app.services.nyt_service import NYTService
from app.services.sentiment_service import SentimentService
import logging
import os
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
logger.info("Loading environment variables...")
load_dotenv()

# After load_dotenv()
# print("All environment variables:", dict(os.environ))

nyt_api_key = os.getenv("NYT_API_KEY")
if nyt_api_key:
    logger.info("NYT API key found in environment variables")
else:
    logger.error("NYT API key not found in environment variables")
    logger.info(f"Current working directory: {os.getcwd()}")
    logger.info(f"Files in current directory: {os.listdir('.')}")

app = FastAPI(title="News Sentiment Analysis API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
try:
    nyt_service = NYTService()
    sentiment_service = SentimentService()
    logger.info("Services initialized successfully")
except Exception as e:
    logger.error(f"Error initializing services: {e}")
    nyt_service = None
    sentiment_service = None

class NewsArticle(BaseModel):
    title: str
    abstract: Optional[str]
    url: str
    published_date: str
    sentiment: Optional[dict] = None

class KeywordRequest(BaseModel):
    keywords: List[str]

@app.get("/")
async def read_root():
    return {"message": "News Sentiment Analysis API"}

@app.post("/analyze-sentiment")
async def analyze_sentiment(text: str):
    if not sentiment_service:
        raise HTTPException(status_code=500, detail="Sentiment service not initialized")
    
    try:
        return sentiment_service.analyze_sentiment(text)
    except Exception as e:
        logger.error(f"Error in sentiment analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/news")
async def get_news(keywords: str, begin_date: Optional[str] = None):
    if not nyt_service or not sentiment_service:
        logger.error("Services not initialized")
        raise HTTPException(status_code=500, detail="Services not initialized")
    
    try:
        # Convert comma-separated keywords to list
        keyword_list = [k.strip() for k in keywords.split(",")]
        logger.info(f"Fetching news for keywords: {keyword_list}, begin_date: {begin_date}")
        
        # Fetch articles from NYT
        articles = await nyt_service.fetch_articles(keyword_list, begin_date)
        logger.info(f"Retrieved {len(articles)} articles from NYT")
        
        # Analyze sentiment for each article
        for article in articles:
            try:
                article["sentiment"] = sentiment_service.analyze_sentiment(article["title"])
            except Exception as e:
                logger.error(f"Error analyzing sentiment for article '{article.get('title', '')}': {str(e)}")
                article["sentiment"] = {
                    "sentiment": "neutral",
                    "confidence": 0,
                    "scores": {
                        "positive": 0,
                        "neutral": 1,
                        "negative": 0
                    }
                }
        
        return articles
        
    except Exception as e:
        logger.error(f"Error in get_news: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 