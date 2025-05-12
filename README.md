# Astro Buddy

**Astro Buddy** is a quasar-specific question-answering web app that leverages Retrieval-Augmented Generation (RAG) powered by recent arXiv publications and OpenAI embeddings. Users can enter an OpenAI API key and pose astronomy-related questions directly through the app's frontend.

## Live Demo

[astro-buddy.vercel.app](https://astro-buddy.vercel.app)

## Features

* Scrapes and downloads the 100 most recent arXiv PDFs about quasars
* Embeds paper content using OpenAI's embedding model
* Stores vector embeddings in a Render-hosted PostgreSQL database with pgvector extension
* Serves responses via FastAPI backend with LangChain + PGVector retrieval
* Responsive frontend deployed via Vercel, built with Next.js and Material UI

## Deployment Overview

* **Frontend**: Vercel (Next.js)
* **Backend**: Render (FastAPI)
* **Database**: Render PostgreSQL with pgvector

## Local Development

1. **Clone the repo:**

```bash
git clone https://github.com/dangause/astro-buddy.git
cd astro-buddy
```

2. **Set up environment variables:**
   Create a `.env.config` file at the root:

```env
OPENAI_API_KEY=sk-...
POSTGRES_DB_HOST=your-db-host
POSTGRES_DB_PORT=5432
POSTGRES_DB_USER=your-user
POSTGRES_DB_PASSWORD=your-password
POSTGRES_DB_DBNAME=your-db
PGVECTOR_COLLECTION_NAME=arxiv_quasars
```

3. **Build services with Docker Compose:**

```bash
docker-compose up --build
```

4. **Access Services:**

* Frontend: [http://localhost:3000](http://localhost:3000)
* Backend API: [http://localhost:8000](http://localhost:8000)
* Data Ingestion API: [http://localhost:8001](http://localhost:8001)
* pgAdmin: [http://localhost:8887](http://localhost:8887)

## How to Ingest Data

Send a `POST` request to:

```
http://localhost:8001/ingest-arxiv
```

This pulls the most recent 100 quasar-related papers from arXiv, embeds the text content, and stores it in the PostgreSQL database.

## Querying

Use the web frontend to input a question and your OpenAI API key.
Alternatively, you can query the backend directly:

```bash
curl -X POST https://astro-buddy.onrender.com/chat-rag \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-..." \
  -d '{"userInput": "What is a quasar?"}'
```

## Credits

Developed by [Dan Gause](https://dangause.com) as part of an astronomy + AI portfolio.

## License

MIT
