# Research: Physical AI & Humanoid Robotics Textbook

**Feature**: 001-physical-ai-textbook
**Date**: 2026-02-21
**Phase**: 0 — Outline & Research

---

## Decision 1: Static Site Framework

**Decision**: Docusaurus 3 (React + MDX)
**Rationale**: First-class support for multi-module documentation with sidebar
navigation, search, versioning, and MDX for embedding React components (the
chatbot widget). Vercel deploys it as a static export with zero configuration.
**Alternatives considered**:
- VitePress — Vue ecosystem, no React component embedding without plugins
- Nextra — Next.js-based, heavier, more complex Vercel config
- MkDocs — Python ecosystem, no React interop

---

## Decision 2: LLM Provider & Models

**Decision**: OpenAI `gpt-4o-mini` (chat) + `text-embedding-3-small` (embeddings)
**Rationale**: gpt-4o-mini gives strong reasoning at low cost (~$0.15/1M input
tokens) — appropriate for a hackathon. `text-embedding-3-small` (1536-dim)
is cheaper than `text-embedding-3-large` while sufficient for a small corpus.
**Alternatives considered**:
- `gpt-4o` — 10× more expensive, overkill for factual Q&A
- Anthropic Claude — no native Python embedding API; requires separate model
- Open-source Llama — requires GPU infra; incompatible with Vercel Functions

---

## Decision 3: Vector Store

**Decision**: Qdrant Cloud (free cluster, 1 collection)
**Rationale**: Qdrant has a free-tier cloud cluster, an official Python SDK,
supports payload filters (for module-level scoping), and is production-ready.
No local setup needed — cluster URL + API key from environment variables.
**Alternatives considered**:
- Pinecone — free tier limited to 1 index, slower cold start
- Weaviate — heavier client, less ergonomic Python SDK
- Chroma (local) — not deployable to Vercel serverless

---

## Decision 4: Relational Database for Chat History

**Decision**: Neon Postgres (serverless, free tier)
**Rationale**: Neon provides a serverless Postgres endpoint with a connection
pool compatible with Vercel's stateless Function environment. The `asyncpg`
driver works well with FastAPI's async event loop.
**Alternatives considered**:
- PlanetScale (MySQL) — incompatible with asyncpg
- Supabase — works but more overhead; Neon is simpler for pure Postgres
- SQLite — not viable for Vercel serverless (no persistent filesystem)

---

## Decision 5: Backend Framework & Deployment

**Decision**: FastAPI (Python 3.11) deployed as Vercel Python Serverless Function
**Rationale**: FastAPI's async-first design matches Vercel's serverless model.
The `api/index.py` entry point pattern is well-documented for Vercel + FastAPI.
ASGI adapter (`mangum`) bridges Vercel's Lambda-style invocation to ASGI.
**Alternatives considered**:
- Flask — synchronous, worse performance for concurrent embedding calls
- Django — too heavy for a single-endpoint chatbot service
- Separate Railway/Render service — adds a second deployment target to manage

---

## Decision 6: Chunking Strategy

**Decision**: 500-token chunks with 50-token overlap, split on sentence
boundaries using `tiktoken` (cl100k_base encoder)
**Rationale**: 500 tokens fits comfortably within gpt-4o-mini's 128k context
while providing enough semantic context per chunk. 50-token overlap preserves
continuity at chunk boundaries. Sentence-boundary splitting avoids cutting
mid-sentence.
**Alternatives considered**:
- Fixed character splits — language-agnostic but ignores sentence structure
- Paragraph splits — chunks vary wildly in size; some too large for embeddings
- 256-token chunks — more chunks, higher Qdrant storage, marginal recall gain

---

## Decision 7: Chatbot Widget Integration

**Decision**: React component in `src/theme/` (Docusaurus swizzle) rendered
as a fixed-position floating panel on every page
**Rationale**: Docusaurus swizzling allows injecting a persistent component
into the root layout without modifying individual MDX files. The widget
communicates with the FastAPI backend via `fetch('/api/chat')`.
**Alternatives considered**:
- MDX import on each page — requires editing every chapter file
- Docusaurus plugin — more complex to scaffold, same outcome
- iFrame embed — CORS issues, poor UX

---

## Decision 8: Content Architecture (4 Modules)

**Decision**:
1. **Foundations of Physical AI** — definitions, history, embodiment hypothesis,
   key systems (Boston Dynamics, Tesla Optimus), safety principles
2. **Sensing & Perception** — sensor modalities (LiDAR, cameras, IMUs, tactile),
   sensor fusion, SLAM, computer vision for robotics, dataset pipelines
3. **Actuation & Control** — actuator types (electric, hydraulic, pneumatic),
   kinematics/dynamics, PID and model-predictive control, reinforcement learning
   for control
4. **Humanoid Robots & Future Directions** — architecture of humanoid platforms,
   loco-manipulation, whole-body control, AI+robotics convergence, ethics

Each module: 3–4 chapters, each chapter: intro + theory + application + summary.

---

## Resolved NEEDS CLARIFICATION items

| Item | Resolution |
|------|-----------|
| Auth method for chatbot | No auth — anonymous public access for hackathon |
| Session persistence strategy | UUID v4 in localStorage; server stores turns in Postgres |
| Deployment of FastAPI on Vercel | `api/index.py` + `mangum` ASGI adapter |
