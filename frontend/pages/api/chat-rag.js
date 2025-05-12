export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).end(); // Method Not Allowed
  }

  const { userInput } = req.body;

  if (!userInput) {
    return res.status(400).json({ error: 'Missing userInput' });
  }

  const apiKey = req.headers.authorization;

  if (!apiKey) {
    return res.status(400).json({ error: 'Missing Authorization header' });
  }

  try {
    const backendUrl = process.env.BACKEND_URL;

    const response = await fetch(`${backendUrl}/chat-rag/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`, // ✅ <-- FIXED HERE
      },
      body: JSON.stringify({ userInput }),
    });

    const text = await response.text();
    console.log('⬅️ Raw backend response:', text);

    let data;
    try {
      data = JSON.parse(text);
    } catch (e) {
      console.error('❌ JSON parse failed');
      return res.status(response.status).json({
        error: `Non-JSON backend response: ${text}`,
      });
    }

    if (!response.ok) {
      console.error('⚠️ Backend returned error:', data);
      return res.status(response.status).json(data);
    }

    return res.status(200).json(data);
  } catch (error) {
    console.error('🔥 Error talking to backend:', error);
    return res.status(500).json({ error: 'Internal Server Error' });
  }
}
