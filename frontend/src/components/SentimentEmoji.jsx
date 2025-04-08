import React from 'react';
import { Typography } from '@mui/material';

function SentimentEmoji({ sentiment }) {
  const getEmoji = () => {
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
    <Typography
      variant="h4"
      component="span"
      sx={{
        display: 'inline-block',
        transition: 'transform 0.2s',
        '&:hover': {
          transform: 'scale(1.2)',
        },
      }}
    >
      {getEmoji()}
    </Typography>
  );
}

export default SentimentEmoji; 