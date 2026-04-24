"""
MedAssistant - RAG-powered Medical Chatbot Backend
FastAPI + TF-IDF RAG + Anthropic Claude API
"""

import json
import math
import re
import os
from pathlib import Path
from typing import List, Optional
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
#from huggingface_hub import InferenceClient
from groq import Groq


# ── App Setup ──────────────────────────────────────────────────────────────────
app = FastAPI(title="MedAssistant API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Data Models ────────────────────────────────────────────────────────────────
class ChatMessage(BaseModel):
    role: str  # "user" | "assistant"
    content: str

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = []

class ChatResponse(BaseModel):
    answer: str
    sources: List[dict]
    confidence: float

class Document(BaseModel):
    id: str
    category: str
    title: str
    content: str
    source: str

# ── RAG Engine ─────────────────────────────────────────────────────────────────
class MedicalRAG:
    def __init__(self, kb_path: str):
        self.documents: List[Document] = []
        self.tfidf_matrix = []
        self.vocabulary = {}
        self.idf = {}
        self._load_knowledge_base(kb_path)
        self._build_index()

    def _load_knowledge_base(self, path: str):
        with open(path, "r") as f:
            data = json.load(f)
        self.documents = [Document(**d) for d in data]
        print(f"[RAG] Loaded {len(self.documents)} documents")

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-z]{2,}\b', text)
        stopwords = {"the","a","an","is","it","in","on","at","to","for","of","and",
                     "or","but","with","this","that","are","was","were","be","been",
                     "have","has","had","do","does","did","will","would","could",
                     "should","may","might","can","not","no","if","as","by","from"}
        return [t for t in tokens if t not in stopwords]

    def _build_index(self):
        # Build vocabulary
        doc_texts = [f"{d.title} {d.content} {d.category}" for d in self.documents]
        tokenized = [self._tokenize(t) for t in doc_texts]

        vocab = set()
        for tokens in tokenized:
            vocab.update(tokens)
        self.vocabulary = {word: i for i, word in enumerate(sorted(vocab))}

        # Compute TF-IDF
        N = len(self.documents)
        df = {word: 0 for word in self.vocabulary}
        tf_matrix = []

        for tokens in tokenized:
            tf = {}
            token_count = len(tokens) or 1
            for token in tokens:
                tf[token] = tf.get(token, 0) + 1
            for word in tf:
                tf[word] /= token_count
                if word in df:
                    df[word] += 1
            tf_matrix.append(tf)

        self.idf = {word: math.log((N + 1) / (df[word] + 1)) + 1 for word in self.vocabulary}

        self.tfidf_matrix = []
        for tf in tf_matrix:
            tfidf = {word: tf.get(word, 0) * self.idf[word] for word in self.vocabulary}
            norm = math.sqrt(sum(v**2 for v in tfidf.values())) or 1
            self.tfidf_matrix.append({w: v/norm for w, v in tfidf.items()})

        print("[RAG] TF-IDF index built successfully")

    def _query_vector(self, query: str) -> dict:
        tokens = self._tokenize(query)
        tf = {}
        for token in tokens:
            tf[token] = tf.get(token, 0) + 1
        count = len(tokens) or 1
        tfidf = {}
        for word, freq in tf.items():
            if word in self.vocabulary:
                tfidf[word] = (freq / count) * self.idf.get(word, 1)
        norm = math.sqrt(sum(v**2 for v in tfidf.values())) or 1
        return {w: v/norm for w, v in tfidf.items()}

    def _cosine_similarity(self, vec1: dict, vec2: dict) -> float:
        return sum(vec1.get(w, 0) * vec2.get(w, 0) for w in vec1)

    def retrieve(self, query: str, top_k: int = 3) -> List[tuple]:
        """Retrieve top-k most relevant documents for a query."""
        q_vec = self._query_vector(query)
        scores = []
        for i, doc_vec in enumerate(self.tfidf_matrix):
            score = self._cosine_similarity(q_vec, doc_vec)
            scores.append((score, i))
        scores.sort(reverse=True)
        results = []
        for score, idx in scores[:top_k]:
            if score > 0.01:  # threshold
                results.append((self.documents[idx], score))
        return results

    def add_document(self, doc: Document):
        """Dynamically add a document and rebuild index."""
        self.documents.append(doc)
        self._build_index()

# ── Initialize RAG ─────────────────────────────────────────────────────────────
KB_PATH = Path(__file__).parent.parent / "data" / "medical_kb.json"
rag = MedicalRAG(str(KB_PATH))
class Settings:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

settings = Settings()
groq_client = Groq(api_key=settings.GROQ_API_KEY)

# ── Routes ──────────────────────────────────────────────────────────────────────
@app.get("/health")
def health_check():
    return {"status": "ok", "documents": len(rag.documents)}

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    # Step 1: Retrieve relevant context
    retrieved = rag.retrieve(req.message, top_k=3)
    
    sources = [
        {
            "title": doc.title,
            "category": doc.category,
            "source": doc.source,
            "relevance": round(score * 100, 1)
        }
        for doc, score in retrieved
    ]

    context_blocks = "\n\n".join(
        f"[{doc.category}] {doc.title}:\n{doc.content}"
        for doc, _ in retrieved
    ) if retrieved else "No specific articles found in knowledge base."

    confidence = round(retrieved[0][1] * 100, 1) if retrieved else 0.0

    # Step 2: Build conversation history for Claude
    messages = []
    for msg in (req.history or [])[-6:]:  # last 6 turns
        messages.append({"role": msg.role, "content": msg.content})

    # Build RAG prompt
    rag_prompt = f"""You are MedAssistant, a helpful and empathetic AI medical information assistant. You provide accurate, evidence-based health information while always emphasizing that users should consult healthcare professionals for personal medical advice.

RETRIEVED MEDICAL KNOWLEDGE BASE CONTEXT:
{context_blocks}

IMPORTANT GUIDELINES:
- Use the retrieved context above as your primary source of information
- Be clear, compassionate, and use accessible language
- Always recommend professional medical consultation for diagnosis or treatment
- Cite which category/topic your answer is based on
- If the question involves emergency symptoms, clearly state to call 911 or seek emergency care
- Do not diagnose conditions — only provide general health education
- If the retrieved context doesn't fully answer the question, say so honestly

User question: {req.message}"""

    messages.append({"role": "user", "content": rag_prompt})

    # Step 3: Call Hugging Face API
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are MedAssistant, a helpful AI health information assistant. Use the retrieved context to answer accurately. Always recommend consulting a doctor."
                },
                {
                    "role": "user",
                    "content": f"CONTEXT:\n{context_blocks}\n\nQUESTION: {req.message}"
                }
            ],
            max_tokens=600,
            temperature=0.4,
        )
        answer = (response.choices[0].message.content or "").strip()

    except Exception as e:
        print(f"[GROQ ERROR] {e}")
        raise HTTPException(status_code=500, detail=f"Groq API error: {str(e)}")
    # Step 3: Get response from Claude
    
    return ChatResponse(
        answer=answer,
        sources=sources,
        confidence=confidence
    )

@app.get("/documents")
def list_documents():
    return {
        "count": len(rag.documents),
        "documents": [
            {"id": d.id, "title": d.title, "category": d.category, "source": d.source}
            for d in rag.documents
        ]
    }

@app.post("/documents/upload")
async def upload_document(
    title: str,
    category: str,
    content: str,
    source: str = "User Upload"
):
    """Add a new document to the knowledge base."""
    new_id = str(len(rag.documents) + 1)
    doc = Document(id=new_id, title=title, category=category, content=content, source=source)
    rag.add_document(doc)

    # Persist to JSON
    all_docs = [d.dict() for d in rag.documents]
    with open(KB_PATH, "w") as f:
        json.dump(all_docs, f, indent=2)

    return {"message": "Document added successfully", "id": new_id, "total": len(rag.documents)}

@app.post("/documents/upload-file")
async def upload_file(file: UploadFile = File(...)):
    """Upload a .txt or .json file to add documents."""
    content = await file.read()
    text = content.decode("utf-8")
    filename = file.filename or ""  # ← fixes the Pylance warning

    if filename.endswith(".json"):
        try:
            docs_data = json.loads(text)
            if not isinstance(docs_data, list):
                docs_data = [docs_data]
            added = 0
            for d in docs_data:
                new_id = str(len(rag.documents) + 1)
                doc = Document(
                    id=new_id,
                    title=d.get("title", "Untitled"),
                    category=d.get("category", "General"),
                    content=d.get("content", ""),
                    source=d.get("source", filename)
                )
                rag.add_document(doc)
                added += 1
            return {"message": f"Added {added} documents from JSON", "total": len(rag.documents)}
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON file")
    elif filename.endswith(".txt"):
        new_id = str(len(rag.documents) + 1)
        doc = Document(
            id=new_id,
            title=filename.replace(".txt", "").replace("_", " ").title(),
            category="Uploaded",
            content=text,
            source=filename
        )
        rag.add_document(doc)
        return {"message": "Text file added as document", "total": len(rag.documents)}
    else:
        raise HTTPException(status_code=400, detail="Only .txt and .json files are supported")

# Serve frontend
frontend_path = Path(__file__).parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path / "static")), name="static")

    @app.get("/")
    def serve_frontend():
        return FileResponse(str(frontend_path / "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)