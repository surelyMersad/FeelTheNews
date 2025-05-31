from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from app.services.nyt_service import NYTService
from app.services.sentiment_service import SentimentService

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
except Exception as e:
    print(f"Error initializing services: {e}")
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
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/news")
async def get_news(keywords: str, begin_date: Optional[str] = None):
    if not nyt_service or not sentiment_service:
        raise HTTPException(status_code=500, detail="Services not initialized")
    
    try:
        # Convert comma-separated keywords to list
        keyword_list = [k.strip() for k in keywords.split(",")]
        
        # Fetch articles from NYT
        articles = await nyt_service.fetch_articles(keyword_list, begin_date)
        
        # Analyze sentiment for each article
        for article in articles:
            article["sentiment"] = sentiment_service.analyze_sentiment(article["title"])
        
        return articles
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 