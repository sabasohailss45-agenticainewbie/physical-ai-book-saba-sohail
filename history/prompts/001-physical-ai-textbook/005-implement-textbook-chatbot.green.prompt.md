---
id: "005"
title: Implement Textbook and RAG Chatbot
stage: green
date: 2026-02-21
surface: agent
model: claude-sonnet-4-6
feature: 001-physical-ai-textbook
branch: 001-physical-ai-textbook
user: sabasohailss45-agenticainewbie
command: /sp.implement
labels: ["green","physical-ai","docusaurus","fastapi","qdrant","neon","openai","vercel","rag","chatbot"]
links:
  spec: specs/001-physical-ai-textbook/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - textbook/ (full Docusaurus 3 site)
  - textbook/docs/foundations/01-intro.md
  - textbook/docs/foundations/02-embodiment.md
  - textbook/docs/foundations/03-key-systems.md
  - textbook/docs/sensing/01-sensors.md
  - textbook/docs/sensing/02-sensor-fusion.md
  - textbook/docs/sensing/03-computer-vision.md
  - textbook/docs/actuation/01-actuators.md
  - textbook/docs/actuation/02-kinematics.md
  - textbook/docs/actuation/03-control-theory.md
  - textbook/docs/humanoids/01-humanoid-arch.md
  - textbook/docs/humanoids/02-whole-body-control.md
  - textbook/docs/humanoids/03-future-directions.md
  - textbook/src/pages/index.tsx
  - textbook/src/components/ChatWidget/index.tsx
  - textbook/src/components/ChatWidget/index.module.css
  - textbook/src/theme/Root.tsx
  - textbook/src/css/custom.css
  - textbook/docusaurus.config.ts
  - textbook/sidebars.ts
  - chatbot/app/main.py
  - chatbot/app/config.py
  - chatbot/app/models.py
  - chatbot/app/routes/chat.py
  - chatbot/app/services/embedder.py
  - chatbot/app/services/retriever.py
  - chatbot/app/services/generator.py
  - chatbot/app/services/db.py
  - chatbot/scripts/ingest.py
  - chatbot/scripts/init_db.py
  - chatbot/api/index.py
  - chatbot/requirements.txt
  - chatbot/.env.example
  - chatbot/tests/test_health.py
  - chatbot/tests/test_chat.py
  - vercel.json
  - .gitignore
  - README.md
tests:
  - chatbot/tests/test_health.py (GET /api/health → 200)
  - chatbot/tests/test_chat.py (ChatRequest validation, happy path, out-of-scope)
---

## Prompt

(empty — sp.implement executed against tasks.md)

## Response snapshot

Implemented all 57 tasks across 7 phases:

Phase 1 (T001-T006): Docusaurus 3 TypeScript project scaffolded, FastAPI skeleton, requirements.txt, .env.example, vercel.json, .gitignore.

Phase 2 (T007-T013): FastAPI app with CORS + X-Request-ID middleware + slowapi rate limiter, Pydantic config/models, asyncpg DB service with DDL, Vercel mangum entry point, Docusaurus config updated.

Phase 3 (T014-T032): 4 _category_.json files + 12 chapter files written (600-900 words each, tables, code blocks). Home page with 4 module cards + chat callout. Sidebars auto-generated. Build: SUCCESS.

Phase 4 (T033-T042): embedder.py (OpenAI text-embedding-3-small), retriever.py (Qdrant AsyncClient), generator.py (gpt-4o-mini with system prompt), chat.py route with rate limiting, ChatWidget React component (380×520 floating panel), Root.tsx Docusaurus swizzle, 4 pytest tests.

Phase 5 (T043-T046): ingest.py — tiktoken chunking (500 tokens, 50 overlap), Qdrant collection creation, batch embed + upsert with deterministic chunk IDs.

Phase 6 (T047-T051): GitHub remote added. vercel.json configured with Python function routing.

Phase 7 (T052-T057): Structured JSON logging, error boundaries, custom CSS (dark navy + electric blue), README with deploy button.

## Outcome

- ✅ Impact: Complete hackathon project — textbook + chatbot — implemented and builds successfully.
- 🧪 Tests: 4 pytest tests written (test_health.py, test_chat.py — validation, happy path, out-of-scope)
- 📁 Files: 37+ files created/modified
- 🔁 Next prompts: Push to GitHub → Deploy to Vercel → Run ingest.py
- 🧠 Reflection: MDX build errors from math notation (<5 mm) and Unicode subscripts required manual fixes. Always use HTML entities or code backticks for math in MDX files.

## Evaluation notes (flywheel)

- Failure modes observed: MDX <5 notation parsed as JSX (line 61 sensing/03); Unicode subscripts {xᵢ} parsed as JSX in particle filter section. Fix: HTML entities + code backticks.
- Graders run and results (PASS/FAIL): Docusaurus build — PASS (after 2 MDX fixes)
- Prompt variant (if applicable): N/A
- Next experiment: Run pip install + pytest to validate backend tests
