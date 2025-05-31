'use client';

import { useState, useEffect } from 'react';
import { format } from 'date-fns';
import DatePicker from 'react-datepicker';
import "react-datepicker/dist/react-datepicker.css";
import { FiRefreshCw, FiSearch, FiPlus, FiTrash2 } from 'react-icons/fi';
import toast from 'react-hot-toast';
import { apiService, Article } from '@/services/api';

const SENTIMENT_EMOJIS = {
  positive: ['😃', '😊', '🙂', '😄', '😁'],
  neutral: ['😐', '🤔', '😶', '😑', '😕'],
  negative: ['😞', '😔', '😟', '😢', '😭']
};

export default function Home() {
  const [articles, setArticles] = useState<Article[]>([]);
  const [keywords, setKeywords] = useState<string[]>([]);
  const [newKeyword, setNewKeyword] = useState('');
  const [selectedDate, setSelectedDate] = useState<Date | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(false);

  // Load saved keywords from localStorage
  useEffect(() => {
    const savedKeywords = localStorage.getItem('keywords');
    if (savedKeywords) {
      setKeywords(JSON.parse(savedKeywords));
    }
  }, []);

  // Save keywords to localStorage
  useEffect(() => {
    localStorage.setItem('keywords', JSON.stringify(keywords));
  }, [keywords]);

  const fetchNews = async () => {
    if (keywords.length === 0) {
      toast.error('Please add at least one keyword');
      return;
    }

    setLoading(true);
    try {
      const data = await apiService.fetchNews(
        keywords,
        selectedDate ? format(selectedDate, 'yyyy-MM-dd') : undefined
      );
      setArticles(data);
    } catch (error) {
      toast.error('Error fetching news');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const addKeyword = () => {
    if (newKeyword.trim() && !keywords.includes(newKeyword.trim())) {
      setKeywords([...keywords, newKeyword.trim()]);
      setNewKeyword('');
    }
  };

  const removeKeyword = (keyword: string) => {
    setKeywords(keywords.filter(k => k !== keyword));
  };

  const getSentimentEmoji = (sentiment: string, confidence: number) => {
    const emojis = SENTIMENT_EMOJIS[sentiment as keyof typeof SENTIMENT_EMOJIS];
    const index = Math.min(Math.floor(confidence * emojis.length), emojis.length - 1);
    return emojis[index];
  };

  const filteredArticles = articles.filter(article =>
    article.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    article.abstract.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <main className="min-h-screen bg-gray-100 dark:bg-gray-900 p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-8">
          News Sentiment Dashboard
        </h1>

        {/* Keywords Section */}
        <div className="bg-white dark:bg-gray-800 rounded-lg p-6 mb-6 shadow-md">
          <h2 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white">
            Keywords
          </h2>
          <div className="flex flex-wrap gap-2 mb-4">
            {keywords.map(keyword => (
              <span
                key={keyword}
                className="bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-100 px-3 py-1 rounded-full flex items-center gap-2"
              >
                {keyword}
                <button
                  onClick={() => removeKeyword(keyword)}
                  className="text-blue-600 dark:text-blue-300 hover:text-blue-800 dark:hover:text-blue-100"
                >
                  <FiTrash2 />
                </button>
              </span>
            ))}
          </div>
          <div className="flex gap-2">
            <input
              type="text"
              value={newKeyword}
              onChange={(e) => setNewKeyword(e.target.value)}
              placeholder="Add new keyword"
              className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
            />
            <button
              onClick={addKeyword}
              className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 flex items-center gap-2"
            >
              <FiPlus /> Add
            </button>
          </div>
        </div>

        {/* Filters Section */}
        <div className="bg-white dark:bg-gray-800 rounded-lg p-6 mb-6 shadow-md">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1">
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Search articles..."
                className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              />
            </div>
            <div className="flex gap-4">
              <DatePicker
                selected={selectedDate}
                onChange={setSelectedDate}
                className="px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                placeholderText="Select date"
              />
              <button
                onClick={fetchNews}
                disabled={loading}
                className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 flex items-center gap-2 disabled:opacity-50"
              >
                <FiRefreshCw className={loading ? 'animate-spin' : ''} />
                {loading ? 'Loading...' : 'Refresh'}
              </button>
            </div>
          </div>
        </div>

        {/* Articles Section */}
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {filteredArticles.map((article, index) => (
            <div
              key={index}
              className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-md hover:shadow-lg transition-shadow"
            >
              <div className="flex items-start justify-between mb-4">
                <span className="text-4xl">
                  {getSentimentEmoji(article.sentiment.sentiment, article.sentiment.confidence)}
                </span>
                <span className="text-sm text-gray-500 dark:text-gray-400">
                  {format(new Date(article.published_date), 'MMM d, yyyy')}
                </span>
              </div>
              <h3 className="text-lg font-semibold mb-2 text-gray-900 dark:text-white">
                {article.title}
              </h3>
              <p className="text-gray-600 dark:text-gray-300 mb-4">
                {article.abstract}
              </p>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-500 dark:text-gray-400">
                  Confidence: {(article.sentiment.confidence * 100).toFixed(1)}%
                </span>
                <a
                  href={article.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-500 hover:text-blue-600 dark:text-blue-400 dark:hover:text-blue-300"
                >
                  Read more
                </a>
              </div>
            </div>
          ))}
        </div>

        {filteredArticles.length === 0 && !loading && (
          <div className="text-center py-12 text-gray-500 dark:text-gray-400">
            No articles found. Add keywords and click refresh to fetch news.
          </div>
        )}
      </div>
    </main>
  );
} 