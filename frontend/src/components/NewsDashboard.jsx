import React from 'react';
import { useQuery } from 'react-query';
import { Grid, Card, CardContent, Typography, IconButton, Box } from '@mui/material';
import RefreshIcon from '@mui/icons-material/Refresh';
import { format } from 'date-fns';
import NewsCard from './NewsCard';
import { fetchNews, refreshNews } from '../services/api';

function NewsDashboard() {
  const { data: articles, isLoading, error, refetch } = useQuery(
    'news',
    fetchNews,
    {
      refetchInterval: 600000, // Refetch every 10 minutes
    }
  );

  const handleRefresh = async () => {
    await refreshNews();
    refetch();
  };

  if (isLoading) {
    return <Typography>Loading...</Typography>;
  }

  if (error) {
    return <Typography color="error">Error loading news: {error.message}</Typography>;
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4" component="h1">
          News Sentiment Dashboard
        </Typography>
        <IconButton onClick={handleRefresh} color="primary">
          <RefreshIcon />
        </IconButton>
      </Box>
      
      <Grid container spacing={3}>
        {articles?.map((article) => (
          <Grid item xs={12} sm={6} md={4} key={article.url}>
            <NewsCard article={article} />
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}

export default NewsDashboard; 