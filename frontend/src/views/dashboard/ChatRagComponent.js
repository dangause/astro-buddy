// components/ChatRagComponent.js
import { useState } from 'react';
import {
  Card,
  CardHeader,
  CardContent,
  Grid,
  TextField,
  Button,
  Typography,
  CircularProgress
} from '@mui/material';
import MuiMarkdown from 'mui-markdown';

const ChatRagComponent = () => {
  const [apiKey, setApiKey] = useState('');
  const [userInput, setUserInput] = useState('');
  const [processedInput, setProcessedInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleApiKeyChange = (e) => {
    setApiKey(e.target.value);
  };

  const handleInputChange = (e) => {
    setUserInput(e.target.value);
  };

  const handleChatRag = async () => {
    setLoading(true);

    if (!apiKey) {
      alert("Please enter your OpenAI API key.");
      setLoading(false);

      return;
    }

    try {
      const response = await fetch('/api/chat-rag/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': apiKey,
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
      setProcessedInput("⚠️ Error: " + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card>
      <CardHeader title="Quasar Query Machine" />
      <CardContent sx={{ pt: (theme) => `${theme.spacing(3)} !important` }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12}>
            <TextField
              label="OpenAI API Key"
              fullWidth
              type="password"
              value={apiKey}
              onChange={handleApiKeyChange}
              placeholder="sk-..."
            />
          </Grid>
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
            <Typography variant="body1" gutterBottom style={{ whiteSpace: 'pre-line' }}>
              Processed Input:
            </Typography>
            {loading ? (
              <CircularProgress size={20} />
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
