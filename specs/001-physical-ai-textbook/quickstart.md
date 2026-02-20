# Quickstart Guide: Physical AI & Humanoid Robotics Textbook

**Feature**: 001-physical-ai-textbook
**Date**: 2026-02-21

---

## Prerequisites

- Node.js 20+ and npm
- Python 3.11+
- Accounts: OpenAI, Qdrant Cloud, Neon (Postgres), Vercel, GitHub

---

## 1 — Clone & Install

```bash
git clone https://github.com/sabasohailss45-agenticainewbie/physical-ai-book-saba-sohail.git
cd physical-ai-book-saba-sohail

# Frontend (Docusaurus)
cd textbook && npm install && cd ..

# Backend (FastAPI)
cd chatbot && pip install -r requirements.txt && cd ..
```

---

## 2 — Configure Environment

```bash
# Copy and fill the example env file
cp chatbot/.env.example chatbot/.env
```

Edit `chatbot/.env`:

```env
OPENAI_API_KEY=sk-...
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your-qdrant-api-key
DATABASE_URL=postgresql://user:pass@host/dbname?sslmode=require
```

---

## 3 — Initialize Database

```bash
cd chatbot
python -m scripts.init_db
```

Expected output:
```
✅ Table conversation_turns created (or already exists)
```

---

## 4 — Ingest Textbook Content

```bash
cd chatbot
python -m scripts.ingest --docs-dir ../textbook/docs
```

Expected output:
```
📄 Processing module: foundations ...
  ✅ foundations-intro: 12 chunks upserted
  ✅ foundations-embodiment: 9 chunks upserted
  ...
✅ Ingestion complete. Total chunks: 148
```

---

## 5 — Start Local Development

**Terminal 1 — FastAPI backend:**
```bash
cd chatbot
uvicorn app.main:app --reload --port 8000
```

Verify: `curl http://localhost:8000/api/health`
Expected: `{"status":"ok"}`

**Terminal 2 — Docusaurus site:**
```bash
cd textbook
npm run start
```

Visit: `http://localhost:3000`

---

## 6 — Test the Chatbot

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is a humanoid robot?", "session_id": "550e8400-e29b-41d4-a716-446655440000"}'
```

Expected: JSON response with `answer` field containing a non-empty string.

---

## 7 — Deploy to Vercel

```bash
# Push to GitHub
git add . && git commit -m "feat: initial textbook + chatbot"
git push origin 001-physical-ai-textbook

# Deploy via Vercel CLI
npm i -g vercel
vercel --prod
```

Set the following environment variables in Vercel dashboard:
- `OPENAI_API_KEY`
- `QDRANT_URL`
- `QDRANT_API_KEY`
- `DATABASE_URL`

---

## Validation Checklist

- [ ] `GET /api/health` returns `{"status":"ok"}`
- [ ] Home page loads at `http://localhost:3000`
- [ ] All 4 module cards are visible on the home page
- [ ] Clicking a module shows at least 3 chapter links in sidebar
- [ ] Chatbot widget is visible on every page
- [ ] Chatbot returns a response to "What is a humanoid robot?"
- [ ] Chatbot politely declines an out-of-scope question
- [ ] Rate limiter returns 429 after 20 requests/min
- [ ] Vercel deployment URL is accessible with HTTPS
