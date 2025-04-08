import React from 'react';
import { Card, CardContent, Typography, Link, Box } from '@mui/material';
import SentimentEmoji from './SentimentEmoji';

function NewsCard({ article }) {
  const getSentimentEmoji = (sentiment) => {
    switch (sentiment) {
      case 'positive':
        return '😃';
      case 'neutral':
        return '😐';
      case 'negative':
        return '😞';
      default:
        return '❓';
    }
  };

  return (
    <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <SentimentEmoji sentiment={article.sentiment} />
          <Typography variant="subtitle2" color="text.secondary" sx={{ ml: 1 }}>
            {Math.round(article.confidence * 100)}% confidence
          </Typography>
        </Box>
        
        <Typography variant="h6" component="h2" gutterBottom>
          {article.title}
        </Typography>
        
        <Typography variant="body2" color="text.secondary" paragraph>
          {article.content}
        </Typography>
        
        <Typography variant="caption" color="text.secondary" display="block">
          {new Date(article.published_date).toLocaleDateString()}
        </Typography>
        
        <Link
          href={article.url}
          target="_blank"
          rel="noopener noreferrer"
          sx={{ mt: 2, display: 'block' }}
        >
          Read more
        </Link>
      </CardContent>
    </Card>
  );
}

export default NewsCard; 