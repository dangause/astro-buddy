// pages/api/chat-rag.js
export default async function handler(req, res) {
  if (req.method === 'POST') {
    const { userInput } = req.body;

    try {
      // Use the backend service name for internal communication in Docker
      const response = await fetch('http://backend:8000/chat-rag', {
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
      res.status(200).json(result);
    } catch (error) {
      console.error('Error fetching data from the server:', error);
      res.status(500).json({ error: 'Internal Server Error' });
    }
  } else {
    res.status(405).end(); // Method Not Allowed
  }
}
