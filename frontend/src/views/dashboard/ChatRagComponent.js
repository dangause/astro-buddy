// components/ChatRagComponent.js
import { useState } from 'react';
import { Card, CardHeader, CardContent, Grid, TextField, Button, Typography, CircularProgress, Box } from '@mui/material';

import MuiMarkdown from 'mui-markdown';

const ChatRagComponent = () => {
  const [userInput, setUserInput] = useState('');
  const [processedInput, setProcessedInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleInputChange = (e) => {
    setUserInput(e.target.value);
  };

  const handleChatRag = async () => {
    setLoading(true); // Set loading to true before the API call

    try {
      const response = await fetch('/api/chat-rag', {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ userInput }),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch data from the server');
      }

      const result = await response.json();
      setProcessedInput(result.response);
    } catch (error) {
      console.error('Error processing response:', error);
    } finally {
      setLoading(false); // Set loading to false after the API call completes (success or error)
    }
  };

  return (
    <Card>
      <CardHeader title='Quasar Query Machine' />
      <CardContent sx={{ pt: (theme) => `${theme.spacing(3)} !important` }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={8}>
            <TextField
              label="User Input"
              fullWidth
              value={userInput}
              onChange={handleInputChange}
            />
          </Grid>
          <Grid item xs={4}>
            <Button variant="contained" onClick={handleChatRag}>
              Process Input
            </Button>
          </Grid>
          <Grid item xs={12}>
          <Typography variant="body1" gutterBottom  style={{whiteSpace: 'pre-line'}}/>
            <Typography variant="body1" gutterBottom  style={{whiteSpace: 'pre-line'}}>
              Processed Input:
            </Typography>
            {loading ? (
              <CircularProgress size={20} /> // Render loading spinner while the API call is in progress
            ) : (
              <MuiMarkdown>{processedInput}</MuiMarkdown>
            )}
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
};

export default ChatRagComponent;
