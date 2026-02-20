---
id: "001"
title: Physical AI Textbook Constitution
stage: constitution
date: 2026-02-21
surface: agent
model: claude-sonnet-4-6
feature: none
branch: master
user: sabasohailss45-agenticainewbie
command: /sp.constitution
labels: ["constitution","physical-ai","humanoid-robotics","docusaurus","rag","fastapi"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - history/prompts/constitution/001-physical-ai-textbook-constitution.constitution.prompt.md
tests:
  - "N/A — constitution document, no tests"
---

## Prompt

Build a complete Physical AI & Humanoid Robotics textbook using spec-kit-plus. Run /sp.constitution, /sp.specify, /sp.plan, /sp.tasks, and /sp.implement. Then set up Docusaurus, write all 4 modules of content, build a RAG chatbot with FastAPI + Qdrant + Neon Postgres + OpenAI, embed the chatbot in the book, and configure Vercel deployment. GitHub username is sabasohailss45-agenticainewbie, repo name is physical-ai-book-saba-sohail. This is for a hackathon due tomorrow morning.

## Response snapshot

Created `.specify/memory/constitution.md` v1.0.0 with six core principles:
I. Content-First, II. API-Driven RAG, III. Test-First, IV. Twelve-Factor Configuration,
V. Observability & Tracing, VI. Simplicity & Smallest Viable Change.
Technology stack table defined (Docusaurus 3, FastAPI, Qdrant, Neon Postgres, OpenAI, Vercel).
Security requirements and governance section established.

## Outcome

- ✅ Impact: Project constitution ratified at v1.0.0 — governs all subsequent development phases.
- 🧪 Tests: N/A
- 📁 Files: .specify/memory/constitution.md (created/overwritten)
- 🔁 Next prompts: /sp.specify — define feature spec for the textbook + chatbot
- 🧠 Reflection: Constitution covers the full stack (content, RAG, infra) and sets clear security + test-first gates.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment: Run /sp.specify to capture user stories and acceptance criteria
