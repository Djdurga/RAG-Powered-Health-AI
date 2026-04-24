# 🏥 MedAssistant — RAG-Powered Medical Chatbot

<div align="center">

![MedAssistant Banner](https://img.shields.io/badge/MedAssistant-RAG%20Powered-2d6a4f?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZD0iTTEyIDJhMTAgMTAgMCAxIDAgMCAyMEExMCAxMCAwIDAgMCAxMiAyem0xIDEzSDExdi02aDJ2NnptMC04SDExVjVoMnYyeiIgZmlsbD0id2hpdGUiLz48L3N2Zz4=)
![Python](https://img.shields.io/badge/Python-3.9+-3776ab?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLaMA%203-f55036?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**An AI-powered medical chatbot using Retrieval-Augmented Generation (RAG)**  
Built with FastAPI · TF-IDF Search Engine · Groq LLaMA 3 · Vanilla JS Frontend

[Features](#-features) · [Demo](#-demo) · [Installation](#-installation) · [Usage](#-usage) · [API](#-api-reference) · [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [About](#-about)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [API Reference](#-api-reference)
- [Knowledge Base](#-knowledge-base)
- [How RAG Works](#-how-rag-works)
- [Contributing](#-contributing)
- [Disclaimer](#-disclaimer)
- [License](#-license)

---

## 🧠 About

MedAssistant is a **RAG-powered AI health chatbot** that answers medical questions using a curated knowledge base. Instead of relying solely on an LLM's training data, it retrieves the most relevant medical articles first, then uses them as context to generate accurate, grounded answers.

This project is ideal for:
- Learning how RAG (Retrieval-Augmented Generation) works in practice
- Building health information tools
- Exploring FastAPI + LLM integration

> ⚠️ **For educational purposes only.** Not a substitute for professional medical advice.

---

## ✨ Features

- 🔍 **Custom TF-IDF RAG Engine** — Pure Python retrieval, no external vector DB needed
- 💬 **Conversational Chat UI** — Multi-turn conversation with history
- 📎 **Source Citations** — Every answer shows which KB articles were used with relevance scores
- 📚 **Dynamic Knowledge Base** — Add articles via UI, file upload (.txt / .json), or API
- 🚨 **Emergency Detection** — Automatically flags emergency symptoms with 911 alerts
- 🧩 **REST API** — Full FastAPI backend with Swagger docs at `/docs`
- 🎨 **Polished Frontend** — Responsive single-file HTML/CSS/JS UI served by FastAPI

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.9+, FastAPI, Uvicorn |
| **RAG Engine** | Custom TF-IDF (pure Python, no dependencies) |
| **LLM** | Groq API — LLaMA 3.1 8B Instant (free tier) |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Data** | JSON knowledge base (easily extendable) |

---

## 📁 Project Structure

```
medassistant/
├── backend/
│   ├── main.py              # FastAPI app + RAG engine + all API routes
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── index.html           # Full chat UI (served by FastAPI)
│   └── static/              # Static assets folder
├── data/
│   └── medical_kb.json      # Medical knowledge base (12 default articles)
├── start.sh                 # One-command startup script (Mac/Linux)
└── README.md
```

---

## 🚀 Installation

### Prerequisites

- Python 3.9 or higher
- A free [Groq API key](https://console.groq.com) *(takes 1 minute to get)*
- Git

### Step 1 — Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/medassistant.git
cd medassistant
```

### Step 2 — Create a Virtual Environment

```bash
# Create venv
python -m venv venv

# Activate — Mac/Linux
source venv/bin/activate

# Activate — Windows
venv\Scripts\activate
```

### Step 3 — Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 4 — Get a Free Groq API Key

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Navigate to **API Keys → Create API Key**
4. Copy the key (starts with `gsk_...`)

### Step 5 — Set the API Key

**Mac/Linux:**
```bash
export GROQ_API_KEY="gsk_your_key_here"
```

**Windows (PowerShell):**
```powershell
$env:GROQ_API_KEY = "gsk_your_key_here"
```

### Step 6 — Run the Server

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Step 7 — Open the App

```
http://localhost:8000
```

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | Your Groq API key | ✅ Yes |

### VS Code Launch Config (optional)

Create `.vscode/launch.json` to run with **F5**:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Run MedAssistant",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"],
      "cwd": "${workspaceFolder}/backend",
      "env": {
        "GROQ_API_KEY": "gsk_your_key_here"
      }
    }
  ]
}
```

---

## 💻 Usage

### Chat Interface

1. Open `http://localhost:8000`
2. Type a health question or click a quick-topic button
3. MedAssistant retrieves relevant articles and generates an answer
4. Source citations appear below each answer with relevance percentages

### Adding Knowledge

Navigate to the **Knowledge Base** tab to:
- **Manually add** articles using the form
- **Upload `.txt` files** — each file becomes one article
- **Upload `.json` files** — add multiple articles at once

#### JSON Upload Format

```json
[
  {
    "id": "13",
    "category": "Pulmonology",
    "title": "Asthma - Symptoms and Treatment",
    "content": "Asthma is a chronic condition...",
    "source": "Custom"
  }
]
```

---

## 📡 API Reference

Interactive docs available at `http://localhost:8000/docs`

### POST `/chat`

Send a message and get a RAG-powered response.

**Request:**
```json
{
  "message": "What are the symptoms of diabetes?",
  "history": [
    { "role": "user", "content": "Hello" },
    { "role": "assistant", "content": "Hi! How can I help?" }
  ]
}
```

**Response:**
```json
{
  "answer": "Diabetes symptoms include frequent urination...",
  "sources": [
    {
      "title": "Diabetes Mellitus - Types, Symptoms and Management",
      "category": "Endocrinology",
      "source": "MedAssistant KB - Endocrinology",
      "relevance": 87.3
    }
  ],
  "confidence": 87.3
}
```

### GET `/documents`

List all articles in the knowledge base.

### POST `/documents/upload`

Add a document via query parameters.

```bash
curl -X POST "http://localhost:8000/documents/upload?\
title=Asthma&category=Pulmonology&content=Asthma+is..."
```

### POST `/documents/upload-file`

Upload a `.txt` or `.json` file.

```bash
curl -X POST http://localhost:8000/documents/upload-file \
  -F "file=@asthma.txt"
```

### GET `/health`

Check server status.

```json
{ "status": "ok", "documents": 12 }
```

---

## 📚 Knowledge Base

The default knowledge base ships with **12 medical articles**:

| # | Category | Topic |
|---|----------|-------|
| 1 | General Medicine | Fever — Causes and When to Seek Care |
| 2 | Neurology | Headache Types and Management |
| 3 | General Medicine | Common Cold — Symptoms and Treatment |
| 4 | Cardiology | High Blood Pressure (Hypertension) |
| 5 | Endocrinology | Diabetes Mellitus |
| 6 | Emergency Medicine | Chest Pain — Emergency Signs |
| 7 | Immunology | Allergies — Types and Treatment |
| 8 | Orthopedics | Back Pain — Causes and Treatment |
| 9 | Psychiatry | Anxiety and Depression |
| 10 | Infectious Disease | COVID-19 |
| 11 | Gastroenterology | GERD, IBS, and Indigestion |
| 12 | Sleep Medicine | Insomnia and Sleep Hygiene |

---

## 🔬 How RAG Works

```
User Question
      │
      ▼
┌─────────────────────────────────┐
│      TF-IDF Retrieval Engine    │
│                                 │
│  1. Tokenize & normalize query  │
│  2. Compute cosine similarity   │
│     against all KB documents    │
│  3. Return top-3 relevant docs  │
└──────────────┬──────────────────┘
               │  Retrieved Context
               ▼
┌─────────────────────────────────┐
│         Groq LLaMA 3.1          │
│                                 │
│  System prompt +                │
│  Retrieved context +            │
│  Conversation history           │
│         │                       │
│         ▼                       │
│  Grounded, cited answer         │
└─────────────────────────────────┘
```

**Why RAG over plain LLM?**
- ✅ Answers grounded in your specific knowledge base
- ✅ Source citations build user trust
- ✅ Easy to update without retraining
- ✅ Reduces hallucinations on domain-specific topics

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes and commit: `git commit -m "Add your feature"`
4. Push to your branch: `git push origin feature/your-feature`
5. Open a Pull Request

### Ideas for Contributions

- [ ] Add sentence-transformers for better semantic search
- [ ] Integrate ChromaDB or Qdrant as vector store
- [ ] Add PDF ingestion support
- [ ] Add user authentication
- [ ] Add Docker support
- [ ] Add support for multiple languages
- [ ] Write unit tests

---

## ⚠️ Disclaimer

MedAssistant is intended for **educational and informational purposes only**.

- It does **not** provide medical diagnosis
- It does **not** replace professional healthcare advice
- Always consult a **licensed healthcare professional** for medical concerns
- In case of emergency, **call 911** or your local emergency number

---

## 📄 License

This project is licensed under the MIT License.

```
MIT License

Copyright (c) 2025 MedAssistant

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

<div align="center">

Made with ❤️ for learning RAG and AI in healthcare

⭐ Star this repo if you found it helpful!

## 📸 Screenshots

<p align="center">
  <img src="assets/knowledge-base.png" width="800"/>
</p>

<p align="center">
  <img src="assets/chat-ui.png" width="800"/>
</p>

</div>
