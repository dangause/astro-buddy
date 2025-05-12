/* eslint-disable newline-before-return */
// pages/api/chat-rag.js

export default async function handler(req, res) {
  if (req.method === 'POST') {
    const { userInput } = req.body;

    const apiKey = req.headers.authorization;
    const apiBase = req.headers['x-api-base'] || '';
    const apiVersion = req.headers['x-api-version'] || '';
    const deploymentName = req.headers['x-deployment-name'] || '';

    if (!userInput || !apiKey) {
      return res.status(400).json({ error: 'Missing userInput or Authorization header' });
    }

    try {
      const response = await fetch('https://astro-buddy-backend.onrender.com/chat-rag', {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'Authorization': apiKey,
          'x-api-base': apiBase,
          'x-api-version': apiVersion,
          'x-deployment-name': deploymentName,
        },
        body: JSON.stringify({ userInput }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        console.error('Backend error:', errorData);
        return res.status(response.status).json(errorData);
      }

      const result = await response.json();
      res.status(200).json(result);
    } catch (error) {
      console.error('Error fetching data from the server:', error);
      res.status(500).json({ error: 'Internal Server Error' });
    }
  } else {
    res.status(405).end(); // Method Not Allowed
  }
}
