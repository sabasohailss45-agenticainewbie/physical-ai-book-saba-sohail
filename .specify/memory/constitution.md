<!--
SYNC IMPACT REPORT
==================
Version change: (none) → 1.0.0 (initial ratification)
Modified principles: N/A (initial)
Added sections:
  - I. Content-First Principle
  - II. API-Driven RAG
  - III. Test-First (NON-NEGOTIABLE)
  - IV. Twelve-Factor Configuration
  - V. Observability & Tracing
  - VI. Simplicity & Smallest Viable Change
Removed sections: N/A
Templates requiring updates:
  ✅ .specify/templates/plan-template.md  — Constitution Check gate added
  ✅ .specify/templates/spec-template.md  — scope sections aligned
  ✅ .specify/templates/tasks-template.md — task categories aligned
Follow-up TODOs: none
-->

# Physical AI & Humanoid Robotics Textbook — Constitution

## Core Principles

### I. Content-First

Every feature, UI component, and service MUST serve the reader's learning journey.
No infrastructure work ships without a corresponding user-facing benefit
(a page, a chatbot response, or a navigable section).
- Docusaurus pages are the canonical source of truth for all module content.
- Content MUST be accurate, cite real research where possible, and be
  structured as progressive chapters (intro → theory → application → exercises).
- Markdown + MDX are the only accepted authoring formats; no proprietary CMS.

### II. API-Driven RAG (Retrieval-Augmented Generation)

The chatbot backend MUST be a stateless FastAPI service with a clean HTTP contract.
- Embeddings MUST be generated via OpenAI `text-embedding-3-small` (or later).
- Vector storage MUST use Qdrant (cloud or local).
- Conversation history and user sessions MUST be persisted in Neon Postgres.
- The chatbot widget MUST be an isolated React component that communicates
  only via `/api/chat` — no direct DB or vector-store calls from the frontend.
- All LLM calls MUST have explicit `system` prompts referencing textbook content.

### III. Test-First (NON-NEGOTIABLE)

TDD is mandatory for all backend services and API contracts:
- Tests MUST be written and MUST FAIL before any implementation begins.
- Red → Green → Refactor cycle is strictly enforced.
- Minimum coverage: 80% for `chatbot/` service, 60% for content utilities.
- Frontend components require at minimum smoke tests (render without crash).

### IV. Twelve-Factor Configuration

No secrets, API keys, or environment-specific values MUST appear in source code.
- All credentials MUST be loaded from environment variables / `.env` (git-ignored).
- `.env.example` MUST be kept current with every required variable documented.
- Vercel environment variables are the production secret store.
- OPENAI_API_KEY, QDRANT_URL, QDRANT_API_KEY, DATABASE_URL MUST never be
  committed to version control.

### V. Observability & Tracing

Every external call (OpenAI, Qdrant, Postgres) MUST be wrapped with:
- Structured JSON logs (level, timestamp, latency_ms, status).
- Error boundaries that return `{"error": "<message>", "request_id": "<uuid>"}`
  with appropriate HTTP status codes (400/422/500).
- FastAPI middleware MUST attach a `X-Request-ID` header to every response.

### VI. Simplicity & Smallest Viable Change

- YAGNI: do not build features not in the current spec.
- Prefer the smallest diff that satisfies acceptance criteria.
- No premature abstraction — three similar lines of code is better than a
  premature utility function.
- Docusaurus plugins MUST only be added when a page requires a capability
  that plain MDX cannot deliver.

## Technology Stack

| Layer | Technology | Version Constraint |
|---|---|---|
| Documentation site | Docusaurus | ^3.x |
| Frontend language | TypeScript | ^5.x |
| Backend language | Python | ^3.11 |
| API framework | FastAPI | ^0.110 |
| Vector store | Qdrant Cloud | latest stable |
| Relational DB | Neon Postgres | latest (serverless) |
| LLM provider | OpenAI | gpt-4o-mini (default) |
| Deployment | Vercel | latest |
| Package manager | npm (frontend) / pip (backend) | latest LTS |

## Security Requirements

- CORS on FastAPI MUST whitelist only the Vercel deployment domain and `localhost`.
- SQL queries MUST use parameterised statements via `asyncpg` / SQLAlchemy ORM
  — no raw string interpolation.
- User input to the chatbot MUST be sanitised (length cap 2000 chars, strip HTML).
- Rate limiting: chatbot endpoint MUST enforce max 20 req/min per IP via
  `slowapi` or equivalent.

## Development Workflow

1. Feature work MUST start with a spec (`specs/<feature>/spec.md`).
2. Plan (`specs/<feature>/plan.md`) MUST pass Constitution Check before coding.
3. Tasks MUST reference spec user stories (US1, US2 …).
4. Every PR MUST reference the task ID and include a test update.
5. Commit messages follow Conventional Commits: `feat:`, `fix:`, `docs:`, `chore:`.

## Governance

This constitution supersedes all other practices defined in this repository.
Amendments require:
1. A written rationale explaining why the principle change is necessary.
2. A version bump following semantic versioning rules (see below).
3. An update to this file via PR reviewed by at least the project owner.
4. A corresponding ADR if the change is architecturally significant.

**Versioning policy**:
- MAJOR — backward-incompatible removal or redefinition of a principle.
- MINOR — new principle or materially expanded guidance added.
- PATCH — clarifications, wording fixes, typo corrections.

All PRs and code reviews MUST verify compliance with this constitution.

**Version**: 1.0.0 | **Ratified**: 2026-02-21 | **Last Amended**: 2026-02-21
