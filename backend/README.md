# Backend (RAG) for light-streamlit

This backend provides a simple RAG (retrieval-augmented generation) API using:

- OpenAI embeddings: `text-embedding-3-small`
- OpenAI chat model: `gpt-4o-mini`
- LangChain for client helpers
- MongoDB for storing documents and embeddings (client-side similarity in this demo)

## Endpoints

- `GET /api/health` - health check
- `GET /api/ping` - ping
- `POST /api/ingest` - ingest a document (JSON: `{ "text": "...", "metadata": { ... } }`)
- `POST /api/query` - query the dataset (JSON: `{ "question": "...", "top_k": 4 }`)

## Environment variables

Put these in `backend/.env` (already present in this repo):

- `OPEN_API_KEY` (or `OPENAI_API_KEY`): your OpenAI API key
- `MONGO_DB_URI`: your MongoDB connection string (e.g., Atlas URI)
- `MONGO_DB`: optional DB name (default: `light_streamlit`)
- `MONGO_COLLECTION`: optional collection name (default: `documents`)

Note: This demo stores embeddings in MongoDB and does client-side cosine similarity. For production-level vector search use MongoDB Atlas Vector Search and implement retrieval with the `$search`/`$knn` operator.

## Install & Run

From the repo root (or inside `backend/`):

```bash
python -m pip install -r backend/requirements.txt
# then run the server:
uvicorn backend.app.main:app --reload --port 8000
```

## Quick test (after starting server)

Ingest:

```bash
curl -X POST http://127.0.0.1:8000/api/ingest -H "Content-Type: application/json" -d '{"text":"This is a small test document about cats.","metadata":{"title":"cats"}}'
```

Query:

```bash
curl -X POST http://127.0.0.1:8000/api/query -H "Content-Type: application/json" -d '{"question":"What is this doc about?","top_k":1}'
```
