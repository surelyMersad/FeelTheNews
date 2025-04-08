import React, { useState } from 'react';
import {
  Box,
  TextField,
  Button,
  Grid,
  Paper,
  Typography,
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { useQuery } from 'react-query';
import { searchNews } from '../services/api';

function FilterPanel() {
  const [searchQuery, setSearchQuery] = useState('');
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);

  const { refetch } = useQuery(
    ['search', searchQuery, startDate, endDate],
    () => searchNews(searchQuery, startDate, endDate),
    {
      enabled: false,
    }
  );

  const handleSearch = () => {
    refetch();
  };

  const handleReset = () => {
    setSearchQuery('');
    setStartDate(null);
    setEndDate(null);
    refetch();
  };

  return (
    <Paper sx={{ p: 3, mb: 3 }}>
      <Typography variant="h6" gutterBottom>
        Filter News
      </Typography>
      
      <Grid container spacing={2}>
        <Grid item xs={12} md={4}>
          <TextField
            fullWidth
            label="Search"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search in article titles..."
          />
        </Grid>
        
        <Grid item xs={12} md={3}>
          <DatePicker
            label="Start Date"
            value={startDate}
            onChange={setStartDate}
            renderInput={(params) => <TextField {...params} fullWidth />}
          />
        </Grid>
        
        <Grid item xs={12} md={3}>
          <DatePicker
            label="End Date"
            value={endDate}
            onChange={setEndDate}
            renderInput={(params) => <TextField {...params} fullWidth />}
          />
        </Grid>
        
        <Grid item xs={12} md={2}>
          <Box sx={{ display: 'flex', gap: 1 }}>
            <Button
              variant="contained"
              onClick={handleSearch}
              fullWidth
            >
              Search
            </Button>
            <Button
              variant="outlined"
              onClick={handleReset}
              fullWidth
            >
              Reset
            </Button>
          </Box>
        </Grid>
      </Grid>
    </Paper>
  );
}

export default FilterPanel; 