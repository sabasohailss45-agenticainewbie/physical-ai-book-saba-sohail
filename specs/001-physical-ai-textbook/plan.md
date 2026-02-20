# Implementation Plan: Physical AI & Humanoid Robotics Textbook

**Branch**: `001-physical-ai-textbook` | **Date**: 2026-02-21 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-physical-ai-textbook/spec.md`

---

## Summary

Build an interactive Physical AI & Humanoid Robotics textbook deployed to Vercel.
The site uses Docusaurus 3 for four content modules and embeds a RAG chatbot
(FastAPI + Qdrant + Neon Postgres + OpenAI gpt-4o-mini) as a floating widget
accessible from every page.

---

## Technical Context

**Language/Version**: Python 3.11 (backend), TypeScript 5.x (frontend)
**Primary Dependencies**: FastAPI 0.110+, Docusaurus 3.x, Qdrant Python SDK,
  asyncpg, openai-python, tiktoken, mangum, slowapi
**Storage**: Neon Postgres (conversation history), Qdrant Cloud (vector store)
**Testing**: pytest + httpx (backend), no frontend test suite for hackathon scope
**Target Platform**: Vercel (static export + Python serverless function)
**Project Type**: Web application (Docusaurus frontend + FastAPI backend)
**Performance Goals**: Chat response < 10 s p95; page load < 3 s on 4G
**Constraints**: OpenAI free/paid tier; Qdrant Cloud free cluster; Neon free tier;
  Vercel Hobby plan; rate limit 20 req/min per IP
**Scale/Scope**: Hackathon demo — single-digit concurrent users; ~150 vector chunks

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Gate | Status |
|-----------|------|--------|
| I. Content-First | Every feature serves reader journey; Docusaurus is canonical | ✅ PASS |
| II. API-Driven RAG | FastAPI + `/api/chat`; Qdrant; Neon; widget isolated | ✅ PASS |
| III. Test-First | pytest tests written before implementation (backend) | ✅ PASS |
| IV. Twelve-Factor Config | All secrets via env vars; `.env.example` kept current | ✅ PASS |
| V. Observability | Structured logs + X-Request-ID + error boundaries | ✅ PASS |
| VI. Simplicity | Smallest viable diff; no extra plugins or abstractions | ✅ PASS |

*All gates pass. Proceeding to design.*

---

## Project Structure

### Documentation (this feature)

```text
specs/001-physical-ai-textbook/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/
│   └── chat-api.yaml   # OpenAPI 3.1 contract
├── checklists/
│   └── requirements.md
└── tasks.md             # Phase 2 output (/sp.tasks)
```

### Source Code (repository root)

```text
textbook/                         # Docusaurus 3 site
├── docusaurus.config.ts
├── sidebars.ts
├── package.json
├── tsconfig.json
├── static/
│   └── img/
├── src/
│   ├── components/
│   │   └── ChatWidget/
│   │       ├── index.tsx         # Floating chat widget
│   │       └── index.module.css
│   ├── css/
│   │   └── custom.css
│   └── pages/
│       └── index.tsx             # Home page with module cards
└── docs/
    ├── foundations/              # Module 1
    │   ├── _category_.json
    │   ├── 01-intro.md
    │   ├── 02-embodiment.md
    │   └── 03-key-systems.md
    ├── sensing/                  # Module 2
    │   ├── _category_.json
    │   ├── 01-sensors.md
    │   ├── 02-sensor-fusion.md
    │   └── 03-computer-vision.md
    ├── actuation/                # Module 3
    │   ├── _category_.json
    │   ├── 01-actuators.md
    │   ├── 02-kinematics.md
    │   └── 03-control-theory.md
    └── humanoids/                # Module 4
        ├── _category_.json
        ├── 01-humanoid-arch.md
        ├── 02-whole-body-control.md
        └── 03-future-directions.md

chatbot/                          # FastAPI RAG backend
├── app/
│   ├── main.py                   # FastAPI app entry point
│   ├── config.py                 # Pydantic settings (env vars)
│   ├── models.py                 # Pydantic request/response models
│   ├── routes/
│   │   └── chat.py               # POST /api/chat, GET /api/health
│   └── services/
│       ├── embedder.py           # OpenAI embeddings
│       ├── retriever.py          # Qdrant vector search
│       ├── generator.py          # OpenAI chat completion
│       └── db.py                 # Neon Postgres session
├── scripts/
│   ├── ingest.py                 # Chunking + Qdrant upsert
│   └── init_db.py                # Postgres DDL
├── tests/
│   ├── test_health.py
│   └── test_chat.py
├── requirements.txt
├── .env.example
└── api/
    └── index.py                  # Vercel Python Function entry point

vercel.json                       # Vercel routing config
.env.example                      # Root env example (reference)
```

**Structure Decision**: Web application layout. `textbook/` is the Docusaurus
static site; `chatbot/` is the FastAPI service deployed as a Vercel Python
Serverless Function under `/api/*`. `vercel.json` routes static assets to the
Docusaurus build output and `/api/*` to the Python function.

---

## Complexity Tracking

> No constitution violations — table not required.

---

## Phase 0: Research Summary

See [research.md](./research.md) for full decisions. Key choices:

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Static site | Docusaurus 3 | React/MDX + Vercel static export |
| LLM chat | gpt-4o-mini | Low cost, strong reasoning |
| Embeddings | text-embedding-3-small | 1536-dim, cheap, sufficient |
| Vector store | Qdrant Cloud | Free tier, Python SDK, payload filters |
| Relational DB | Neon Postgres | Serverless, asyncpg, Vercel compatible |
| Backend | FastAPI + mangum | Async, minimal, Vercel Python Function |
| Chunking | 500 tokens, 50 overlap | Balanced context vs. storage |
| Widget | Docusaurus swizzle | Persistent across all pages |

---

## Phase 1: Design

### Data Model

See [data-model.md](./data-model.md). Key entities: Module, Chapter, Chunk
(Qdrant), ConversationTurn (Postgres), Session (localStorage).

### API Contracts

See [contracts/chat-api.yaml](./contracts/chat-api.yaml).
- `GET /api/health` → `{"status":"ok"}`
- `POST /api/chat` → ChatRequest → ChatResponse | ErrorResponse

### Vercel Configuration

```json
{
  "buildCommand": "cd textbook && npm run build",
  "outputDirectory": "textbook/build",
  "functions": {
    "chatbot/api/index.py": {
      "runtime": "python3.11"
    }
  },
  "rewrites": [
    { "source": "/api/(.*)", "destination": "/chatbot/api/index.py" }
  ]
}
```

### FastAPI System Prompt Template

```
You are an expert tutor for the Physical AI & Humanoid Robotics textbook.
Answer ONLY based on the provided context. If the answer is not in the context,
respond: "This topic is not covered in the current textbook modules."

Context:
{context}

Question: {question}
```

---

## Follow-ups & Risks

1. **Vercel Python Function cold start** — mangum adds ~100 ms on first call;
   acceptable for hackathon but warn users in demo.
2. **Qdrant free tier limit** — 1 GB storage; textbook corpus is ~1 MB, safe.
3. **OpenAI rate limits** — gpt-4o-mini has generous RPM limits; use exponential
   backoff in `generator.py` for robustness.
