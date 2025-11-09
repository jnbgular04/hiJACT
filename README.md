# Bill Assistant AI (BAAI) 

A compact Retrieval-Augmented-Generation (RAG) demo: a FastAPI backend that indexes documents with OpenAI embeddings and a Streamlit frontend to ask questions over those documents.

Author: **hiJACT**

Submitted to: **CodeKada by DevKada**

Quick badges / tech stack
------------------------

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-FF5A5F?logo=fastapi&logoColor=white) ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white) ![LangChain](https://img.shields.io/badge/LangChain-%20-2b6cb0) ![OpenAI](https://img.shields.io/badge/OpenAI-000000?logo=openai&logoColor=white) ![MongoDB](https://img.shields.io/badge/MongoDB-47A248?logo=mongodb&logoColor=white)

Overview
--------

- Backend: `backend/` — FastAPI app that ingests documents (CSV/XLSX/JSON/TXT/PDF), generates embeddings with OpenAI, stores vectors & metadata in MongoDB, and serves a simple RAG query API.
- Frontend: `frontend/` — Streamlit UI for uploading documents and chatting with the RAG assistant.

Quickstart (recommended)
------------------------

Prerequisites
- Python 3.10+
- A MongoDB URI (Atlas or local)
- An OpenAI API key

Install & run (from repo root)

1) Setup backend venv and install dependencies

```bash
make setup-backend
```

2) Setup frontend venv and install dependencies

```bash
make setup-frontend
```

3) Start the backend (dev mode)

```bash
make run-backend
```

4) Start the frontend and open http://localhost:8501

```bash
make run-frontend
```

Environment variables
---------------------
Create `backend/.env` (example):

```
OPENAI_API_KEY=sk-...your-openai-key...
MONGO_DB_URI=mongodb+srv://<user>:<pass>@cluster0.example.mongodb.net/
# optional overrides
MONGO_DB=bills_db
MONGO_COLLECTION=bills_collection
```

Notes
-----
- The Makefile creates isolated virtualenvs (`backend/.venv`, `frontend/.venv`) and installs the component dependencies from each `requirements.txt`.

Backend API (summary)
---------------------
- GET `/api/health` — health check
- POST `/api/ingest_text` — ingest a single text document (JSON: `{ "text": "...", "metadata": {...} }`)
- POST `/api/ingest_pdf` — upload a PDF (multipart form `file`) — the server saves the file and embeds the whole PDF as one document
- POST `/api/query` — run a RAG query (JSON: `{ "question": "...", "top_k": 4 }`) — returns `{ "answer": ..., "sources": [...] }`

License
-------
[See License](LICENSE.md)