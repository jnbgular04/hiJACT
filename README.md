# Light Streamlit — RAG backend + Streamlit frontend

This repository contains a small Retrieval-Augmented-Generation (RAG) demo:

- `backend/` — FastAPI backend that embeds documents with OpenAI embeddings, stores them in MongoDB, performs retrieval, and uses an OpenAI chat model for generation. It supports ingesting single documents or file uploads (CSV / XLSX / JSON / TXT) and exporting retrieved sources as CSV.
- `frontend/` — Streamlit chat UI that allows users to upload a bills file, ask questions (the app calls the backend `/api/query`), and download sources for the latest query.

This README explains how to set up and run the project using the included Makefile targets.

Prerequisites
-------------

- Python 3.10+ (the Makefile creates per-component virtualenvs)
- Git (optional)
- A MongoDB instance (Atlas or local). You'll need a connection URI.
- An OpenAI API key.

Makefile targets (recommended)
------------------------------

The repository includes convenient `make` targets that create virtual environments for the backend and frontend and run them. All commands below are intended to be run from the repository root.

1) Setup backend venv and install dependencies

```bash
make setup-backend
```

This creates `backend/.venv` and installs packages from `backend/requirements.txt`.

2) Setup frontend venv and install dependencies

```bash
make setup-frontend
```

This creates `frontend/.venv` and installs packages from `frontend/requirements.txt`.

3) Run the backend

```bash
make run-backend
```

This launches the FastAPI server on port 8000 (dev mode, `--reload`). The server entrypoint is `backend/app/main.py`.

4) Run the Streamlit frontend

```bash
make run-frontend
```

Open the UI at: http://localhost:8501

5) Run both together (setup then start)

```bash
make run-all
```

This runs `setup-backend` and `setup-frontend`, starts the backend in the background, and then starts the frontend in the foreground.

Useful additional targets
------------------------

- `make test` — runs backend tests (if present) after creating backend venv.
- `make clean` — removes created venvs: deletes `backend/.venv`, `frontend/.venv`, and root `.venv`.

Environment variables (.env)
----------------------------

The backend reads sensitive values from `backend/.env`. Create or edit that file with the following values (example):

```
OPENAI_API_KEY=sk-...your-openai-key...
MONGO_DB_URI=mongodb+srv://<user>:<pass>@cluster0.example.mongodb.net/
# optional overrides
MONGO_DB=bills_db
MONGO_COLLECTION=bills_collection
```

Important: Never put the OpenAI key in the frontend code or commit it into Git.

How to use the app (quick flow)
-------------------------------

1. Start backend and frontend as shown above.
2. In the Streamlit UI (http://localhost:8501):
   - Upload a bills file (CSV / XLSX / JSON / TXT) using "Choose a file" → click "Upload & Ingest". Each row/item will be inserted into MongoDB as a document and embedded.
   - Ask questions in the chat box. The frontend sends the question to the backend `/api/query` endpoint, which returns an answer plus a list of retrieved sources.
   - After you get an answer, click "Download sources CSV" to download a CSV containing metadata and text for the top retrieved documents for your last query.

Backend API (useful for debugging)
----------------------------------

- GET `/api/health` — health check
- POST `/api/ingest` — ingest a single text document (JSON: `{ "text": "...", "metadata": {...} }`)
- POST `/api/ingest_file` — ingest an uploaded file (multipart form `file`) — supports CSV/XLSX/JSON/TXT
- POST `/api/query` — run a RAG query (JSON: `{ "question": "...", "top_k": 4 }`) — returns `{ "answer": ..., "sources": [...] }`
- POST `/api/export` — export top sources for a question as CSV (JSON: `{ "question": "...", "top_k": 10 }`) — returns a `text/csv` attachment

Example curl for ingest_file (CSV):

```bash
curl -X POST "http://localhost:8000/api/ingest_file" -F "file=@/path/to/bills.csv"
```

Example curl for query:

```bash
curl -X POST "http://localhost:8000/api/query" -H "Content-Type: application/json" -d '{"question":"Which bills are due next week?","top_k":5}'
```

Troubleshooting
---------------

- If `pip` errors about a system-managed Python environment, ensure you run `make setup-backend` / `make setup-frontend` which create virtual environments and install inside them. You can activate a venv manually:

```bash
source backend/.venv/bin/activate
python -m pip install -r backend/requirements.txt
```

- If the backend cannot connect to MongoDB, double-check `MONGO_DB_URI` in `backend/.env` and that your IP / network access is allowed (for Atlas). Check the server logs for connection errors.
- If embeddings/LLM calls fail, ensure `OPENAI_API_KEY` is set and valid in `backend/.env`.

Development notes & next steps
-----------------------------

- For production, consider switching to a real vector index (MongoDB Atlas Vector Search, FAISS, or a managed vector DB) instead of client-side similarity. Client-side similarity loads the collection into memory and is not suitable for large datasets.
- Consider adding normalization for dates and amounts when ingesting files (so queries like "due next week" can be answered more reliably with structured filtering).
- Add tests for ingestion and query flows to `backend/tests/` and run with `make test`.

License & attribution
---------------------

This project is provided as a small demo/boilerplate. Adapt and extend as needed.
