# News Sentiment Analysis Dashboard

A real-time news sentiment analysis dashboard that uses the New York Times API and FinBERT for sentiment analysis with emoji-based visualization.

## Features

- Real-time news fetching from NYT API
- Sentiment analysis using FinBERT
- Emoji-based sentiment visualization
- User-saved keywords
- Date-based filtering
- Search functionality
- Responsive design
- Dark mode support

## Tech Stack

- Frontend: Next.js 14 with TypeScript
- Styling: Tailwind CSS
- Backend: FastAPI (Python)
- Sentiment Analysis: FinBERT (HuggingFace Transformers)
- News API: New York Times API

## Prerequisites

- Node.js 18+ and npm
- Python 3.8+
- NYT API Key

## Setup Instructions

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env.local` file with your NYT API key:
```
NEXT_PUBLIC_NYT_API_KEY=your_api_key_here
```

4. Start the development server:
```bash
npm run dev
```

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start the FastAPI server:
```bash
uvicorn main:app --reload
```

## Environment Variables

### Frontend (.env.local)
- `NEXT_PUBLIC_NYT_API_KEY`: Your New York Times API key

### Backend (.env)
- `NYT_API_KEY`: Your New York Times API key

## Project Structure

```
news-sentiment-dashboard/
├── frontend/                 # Next.js frontend application
│   ├── src/
│   │   ├── app/             # Next.js app directory
│   │   ├── components/      # React components
│   │   └── lib/            # Utility functions
│   └── public/             # Static assets
└── backend/                # FastAPI backend
    ├── app/
    │   ├── api/           # API routes
    │   ├── models/        # Data models
    │   └── services/      # Business logic
    └── tests/             # Test files
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

MIT 