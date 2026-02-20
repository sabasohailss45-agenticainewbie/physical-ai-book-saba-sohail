---
id: "003"
title: Physical AI Textbook Architecture Plan
stage: plan
date: 2026-02-21
surface: agent
model: claude-sonnet-4-6
feature: 001-physical-ai-textbook
branch: 001-physical-ai-textbook
user: sabasohailss45-agenticainewbie
command: /sp.plan
labels: ["plan","physical-ai","docusaurus","fastapi","qdrant","neon","openai","vercel"]
links:
  spec: specs/001-physical-ai-textbook/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-physical-ai-textbook/plan.md
  - specs/001-physical-ai-textbook/research.md
  - specs/001-physical-ai-textbook/data-model.md
  - specs/001-physical-ai-textbook/quickstart.md
  - specs/001-physical-ai-textbook/contracts/chat-api.yaml
  - history/prompts/001-physical-ai-textbook/003-physical-ai-textbook-plan.plan.prompt.md
tests:
  - "N/A — planning phase"
---

## Prompt

001-physical-ai-textbook

## Response snapshot

Phase 0 research complete: 8 decisions documented (Docusaurus 3, gpt-4o-mini,
text-embedding-3-small, Qdrant Cloud, Neon Postgres, FastAPI+mangum, 500-token
chunks, Docusaurus swizzle widget).

Phase 1 design complete:
- data-model.md: Module, Chapter, Chunk, ConversationTurn, Session entities
- contracts/chat-api.yaml: OpenAPI 3.1 spec for POST /api/chat + GET /api/health
- quickstart.md: end-to-end local dev → Vercel deploy instructions
- plan.md: full project structure (textbook/ + chatbot/), Constitution Check
  all 6 gates PASS, Vercel config, FastAPI system prompt template

Agent context updated in CLAUDE.md.

## Outcome

- ✅ Impact: Architecture fully designed — ready for /sp.tasks.
- 🧪 Tests: N/A at plan stage
- 📁 Files: plan.md, research.md, data-model.md, quickstart.md, contracts/chat-api.yaml
- 🔁 Next prompts: /sp.tasks — generate actionable task list
- 🧠 Reflection: mangum adapter is the key enabler for FastAPI-on-Vercel; Qdrant
  payload filters on module_id will allow scoped retrieval later.

## Evaluation notes (flywheel)

- Failure modes observed: create-new-feature.ps1 parameter error (non-blocking — branch was created)
- Graders run and results (PASS/FAIL): Constitution Check 6/6 PASS
- Prompt variant (if applicable): N/A
- Next experiment: /sp.tasks to generate T001–Txxx implementation task list
