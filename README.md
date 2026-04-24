# 🏥 MedAssistant — RAG-Powered Medical Chatbot

A production-ready AI health assistant built with **FastAPI**, **custom TF-IDF RAG engine**, and **Claude (Anthropic API)**.

---

## 🗂 Project Structure

```
medassistant/
├── backend/
│   ├── main.py              # FastAPI app + RAG engine + all API routes
│   └── requirements.txt     # Python dependencies
├── frontend/
│   └── index.html           # Full chat UI (served by FastAPI)
├── data/
│   └── medical_kb.json      # Medical knowledge base (12 articles, easily extendable)
├── start.sh                 # One-command startup script
└── README.md
```

---
## 📸 Screenshots

<p align="center">
  <img src="assets/knowledge-base.png" width="800"/>
</p>

<p align="center">
  <img src="assets/chat-ui.png" width="800"/>
</p>

## ⚙️ Setup & Run

### 1. Prerequisites

- Python 3.9+
- An Anthropic API key → [console.anthropic.com](https://console.anthropic.com)

### 2. Set API Key

```bash
export ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### 3. Start the App

```bash
cd medassistant
chmod +x start.sh
./start.sh
```

Or manually:

```bash
cd medassistant/backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Open in Browser

```
http://localhost:8000
```

---

## 🧠 How RAG Works (Architecture)

```
User Query
    │
    ▼
┌─────────────────────────────────┐
│    TF-IDF Retrieval Engine      │  ← Pure Python, no external vector DB
│  - Tokenize & normalize query   │
│  - Compute cosine similarity    │
│  - Return top-3 relevant docs   │
└────────────────┬────────────────┘
                 │  Retrieved Context
                 ▼
┌─────────────────────────────────┐
│      Claude (claude-sonnet)     │  ← Anthropic API
│  System prompt + context +      │
│  conversation history           │
│  → Grounded, cited response     │
└─────────────────────────────────┘
```

**Key RAG steps:**
1. User sends a health question
2. TF-IDF engine scores all KB documents against the query
3. Top-3 documents above relevance threshold are retrieved
4. Documents injected as context into Claude's prompt
5. Claude generates a grounded, source-cited answer
6. Frontend displays answer + clickable source chips with relevance %

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/` | Serves the chat UI |
| `GET`  | `/health` | Health check + document count |
| `POST` | `/chat` | Chat with RAG (main endpoint) |
| `GET`  | `/documents` | List all KB documents |
| `POST` | `/documents/upload` | Add a document via form params |
| `POST` | `/documents/upload-file` | Upload .txt or .json file |
| `GET`  | `/docs` | Swagger API documentation |

### Chat Request Example

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are the symptoms of a fever and when should I see a doctor?",
    "history": []
  }'
```

### Chat Response Schema

```json
{
  "answer": "A fever is defined as...",
  "sources": [
    {
      "title": "Fever - Causes and When to Seek Care",
      "category": "Fever",
      "source": "MedAssistant KB - General Medicine",
      "relevance": 87.3
    }
  ],
  "confidence": 87.3
}
```

---

## 📚 Knowledge Base

The default KB ships with **12 medical articles** covering:

| Category | Topics |
|----------|--------|
| General Medicine | Fever, Common Cold |
| Neurology | Headaches, Migraines |
| Cardiology | Hypertension, Chest Pain |
| Endocrinology | Diabetes |
| Immunology | Allergies |
| Orthopedics | Back Pain |
| Psychiatry | Anxiety, Depression |
| Infectious Disease | COVID-19 |
| Gastroenterology | GERD, IBS |
| Sleep Medicine | Insomnia |

### Adding Custom Knowledge

**Option A — UI (easiest):** Go to *Knowledge Base* tab → fill in form → click *Add to Knowledge Base*

**Option B — File upload:** Upload a `.txt` or `.json` file from the UI

**Option C — JSON format:**
```json
[
  {
    "id": "13",
    "category": "Dermatology",
    "title": "Eczema - Triggers and Treatment",
    "content": "Eczema (atopic dermatitis) is a chronic...",
    "source": "Custom"
  }
]
```

**Option D — API:**
```bash
curl -X POST "http://localhost:8000/documents/upload?title=Eczema&category=Dermatology&content=Eczema+is..."
```

---

## 🔒 Safety Features

- Emergency keyword detection → automatic 🚨 banner shown in UI
- Medical disclaimer in sidebar
- Claude instructed to never diagnose — only educate
- Crisis resources mentioned for mental health queries
- All responses recommend professional consultation

---

## 🛠 Extending the Project

| Enhancement | How |
|-------------|-----|
| Better retrieval | Swap TF-IDF for sentence-transformers or OpenAI embeddings |
| Persistent vector store | Add ChromaDB, Qdrant, or Pinecone |
| PDF ingestion | Use `pypdf2` to extract text from medical PDFs |
| User auth | Add FastAPI-Users or JWT middleware |
| Deployment | Docker + Render / Railway / AWS |

---

## ⚠️ Disclaimer

MedAssistant is for **educational purposes only**. It does not provide medical diagnosis or replace professional healthcare. Always consult a licensed physician for medical advice.
