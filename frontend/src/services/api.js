import axios from 'axios';
import { format } from 'date-fns';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const fetchNews = async () => {
  try {
    const response = await api.get('/news/latest/');
    return response.data;
  } catch (error) {
    throw new Error('Failed to fetch news');
  }
};

export const searchNews = async (query, startDate, endDate) => {
  try {
    const params = new URLSearchParams();
    
    if (query) {
      params.append('q', query);
    }
    if (startDate) {
      params.append('start_date', format(startDate, 'yyyy-MM-dd'));
    }
    if (endDate) {
      params.append('end_date', format(endDate, 'yyyy-MM-dd'));
    }
    
    const response = await api.get(`/news/search/?${params.toString()}`);
    return response.data;
  } catch (error) {
    throw new Error('Failed to search news');
  }
};

export const refreshNews = async () => {
  try {
    const response = await api.post('/news/refresh/');
    return response.data;
  } catch (error) {
    throw new Error('Failed to refresh news');
  }
}; 