import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface Article {
  title: string;
  abstract: string;
  url: string;
  published_date: string;
  sentiment: {
    sentiment: string;
    confidence: number;
    scores: {
      positive: number;
      neutral: number;
      negative: number;
    };
  };
}

export interface SentimentAnalysis {
  sentiment: string;
  confidence: number;
  scores: {
    positive: number;
    neutral: number;
    negative: number;
  };
}

class ApiService {
  private static instance: ApiService;
  private api;

  private constructor() {
    this.api = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  public static getInstance(): ApiService {
    if (!ApiService.instance) {
      ApiService.instance = new ApiService();
    }
    return ApiService.instance;
  }

  async fetchNews(keywords: string[], beginDate?: string): Promise<Article[]> {
    try {
      const response = await this.api.get('/news', {
        params: {
          keywords: keywords.join(','),
          begin_date: beginDate,
        },
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching news:', error);
      throw error;
    }
  }

  async analyzeSentiment(text: string): Promise<SentimentAnalysis> {
    try {
      const response = await this.api.post('/analyze-sentiment', { text });
      return response.data;
    } catch (error) {
      console.error('Error analyzing sentiment:', error);
      throw error;
    }
  }
}

export const apiService = ApiService.getInstance(); 