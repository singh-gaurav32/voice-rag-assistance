# Voice RAG Customer-Care Assistant

A voice-enabled customer care assistant that answers user questions using **RAG (Retrieval-Augmented Generation)** from a small FAQ knowledge base.

---

## Features

- **Voice I/O**
  - Convert speech → text (STT)
  - Generate spoken answer (TTS)
  - Basic barge-in support (interrupt assistant speech)
- **RAG Pipeline**
  - Ingests multiple documents (Markdown, text, or FAQ JSON)
  - Stores embeddings in a FAISS vector index
  - Retrieves relevant chunks to answer queries with citations
- **Customer Flows**‸
  - Returns inquiries (FAQ-based)
  - Order status queries (stubbed API)
- **Frontend**
  - Browser demo with mic input + speaker output

---

## Demo

- Hosted backend (Vercel): ``
- Frontend GitHub Pages demo: ``

---

## Setup (Local)

### 1. Clone the repo

```bash
git clone https://github.com/singh-gaurav32/voice-rag-assistance.git
cd voice-rag-assistant/backend
```

### 2. Environment Variables

Create a `.env` file:

```text
GEMINI_API_KEY=your_gemini_api_key
OPENAI_API_KEY=your_openai_api_key
LLM_PROVIDER=gemini
FUZZY_THRESHOLD=80
```

### 3. Setup via docker recommended

```bash
docker compose up
```

### 4. Ingest documents

```bash
docker exec -it fastapi_app uv run -m scripts.ingest_full
```

### 5. Run backend

```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8080
```

### Running the Frontend

You have two options to run the frontend:

1. **Open directly in browser**  
   Simply open the file `frontend/index.html` in your browser.  
   **Note:** Some browsers may block API calls due to `file://` restrictions.

2. **Use a local HTTP server** (recommended)  
   This simulates a real server and avoids CORS issues:

   ```bash
   cd frontend
   python -m http.server 8000
   ```

   Then open http://localhost:8000/index.html in your browser.

---

## Usage

1. Click **Start** to speak your query.
2. The assistant will respond vocally and display the answer.
3. Click **Stop** to halt recognition or speech (barge-in support).

---

---

---

## Notes

- **Model:** `all-MiniLM-L6-v2` for embeddings (CPU-friendly)
- **FAISS index:** stores chunked document embeddings
- **Logging:** logs queries, intents, and answers (`./logs/queries.log`)
- **Barge-in:** user can interrupt assistant speech by clicking Stop/Start

---

---

## License

MIT License
