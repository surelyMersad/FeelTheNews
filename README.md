# News Sentiment Dashboard

A real-time news sentiment analysis dashboard that displays news articles with their sentiment analysis using emojis (😃 😐 😞). The application uses the New York Times API for news data and FinBERT for sentiment analysis.

## Features

- Real-time news updates (every 10 minutes)
- Manual refresh option
- Sentiment analysis with confidence scores
- Emoji-based sentiment visualization
- Date-based filtering
- Keyword search in article titles
- Redis caching for improved performance
- Responsive design

## Project Structure

```
news-sentiment-dashboard/
├── backend/
│   ├── news_api/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── services/
│   │       ├── sentiment_analyzer.py
│   │       ├── news_fetcher.py
│   │       └── cache_manager.py
│   ├── requirements.txt
│   └── manage.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── NewsCard.jsx
│   │   │   ├── SentimentEmoji.jsx
│   │   │   ├── FilterPanel.jsx
│   │   │   └── SearchBar.jsx
│   │   ├── services/
│   │   │   ├── api.js
│   │   │   └── cache.js
│   │   └── App.jsx
│   └── package.json
└── README.md
```

## Prerequisites

- Python 3.8+
- Node.js 14+
- Redis server
- New York Times API key

## Setup Instructions

### Backend Setup

1. Create and activate a virtual environment:
```bash
cd backend
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the backend directory with the following content:
```
NYT_API_KEY=your_nyt_api_key_here
DJANGO_SECRET_KEY=your_django_secret_key_here
REDIS_URL=redis://127.0.0.1:6379/1
```

4. Run database migrations:
```bash
python manage.py migrate
```

5. Start the Django development server:
```bash
python manage.py runserver
```

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm start
```

## API Endpoints

- `GET /api/news/latest/` - Get latest news articles with sentiment analysis
- `GET /api/news/search/` - Search articles with optional date filtering
  - Query parameters:
    - `q`: Search query
    - `start_date`: Start date (YYYY-MM-DD)
    - `end_date`: End date (YYYY-MM-DD)
- `POST /api/news/refresh/` - Force refresh of latest articles

## Technologies Used

### Backend
- Django 5.0.2
- Django REST Framework
- FinBERT (Hugging Face Transformers)
- Redis for caching
- NYT API integration

### Frontend
- React
- Material-UI
- React Query for data fetching
- Axios for API calls

## Caching Strategy

The application uses Redis for caching to:
- Reduce API calls to NYT
- Improve response times
- Handle multiple concurrent users efficiently

Cache duration: 10 minutes (configurable in `cache_manager.py`)

## Error Handling

The application includes comprehensive error handling:
- API request failures
- Sentiment analysis errors
- Cache operation failures
- Input validation

All errors are logged and appropriate error messages are returned to the client.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 