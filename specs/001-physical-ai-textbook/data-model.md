# Data Model: Physical AI & Humanoid Robotics Textbook

**Feature**: 001-physical-ai-textbook
**Date**: 2026-02-21
**Phase**: 1 — Design

---

## Entities

### Module

Represents a top-level section of the textbook.

| Field | Type | Constraints |
|-------|------|-------------|
| id | string | slug format, unique, PK |
| title | string | non-empty, max 100 chars |
| description | string | non-empty, max 500 chars |
| order | integer | ≥ 1, unique |
| chapters | Chapter[] | ordered list |

**Validation**: `id` must be URL-safe slug. `order` determines sidebar position.

---

### Chapter

A single navigable page within a module.

| Field | Type | Constraints |
|-------|------|-------------|
| id | string | slug format, unique within module |
| module_id | string | FK → Module.id |
| title | string | non-empty, max 150 chars |
| slug | string | URL-safe, globally unique |
| content | string | Markdown/MDX source |
| order | integer | ≥ 1, unique within module |

**Validation**: `slug` forms the URL path `/docs/{module_id}/{slug}`.

---

### Chunk (Qdrant vector payload)

A text fragment stored in Qdrant for retrieval.

| Field | Type | Constraints |
|-------|------|-------------|
| chunk_id | string | `{chapter_slug}_{index}` — deterministic, unique |
| chapter_slug | string | FK → Chapter.slug |
| module_id | string | FK → Module.id |
| content | string | 1–500 tokens of text |
| token_count | integer | 1–550 |
| char_offset | integer | byte offset in source file |

**Qdrant collection**: `physical-ai-textbook`
**Vector dimension**: 1536 (text-embedding-3-small)
**Distance metric**: Cosine
**Payload filters**: `module_id`, `chapter_slug` (for scoped search)

---

### ConversationTurn (Neon Postgres)

Persists each chatbot exchange for analytics and conversation history.

| Field | Type | Constraints |
|-------|------|-------------|
| id | UUID | PK, auto-generated |
| session_id | UUID | non-null, indexed |
| question | text | non-empty, max 2000 chars |
| answer | text | non-empty |
| context_chunks | JSONB | array of chunk_ids used |
| prompt_tokens | integer | ≥ 0 |
| completion_tokens | integer | ≥ 0 |
| total_tokens | integer | ≥ 0 |
| model | varchar(50) | e.g. "gpt-4o-mini" |
| created_at | timestamptz | default now() |

**Index**: `(session_id, created_at DESC)` for history retrieval.

---

### Session (client-side + Postgres)

| Field | Type | Constraints |
|-------|------|-------------|
| session_id | UUID | PK, generated client-side (UUID v4) |
| created_at | timestamptz | set on first turn |
| last_active | timestamptz | updated on each turn |

**Storage**: `session_id` stored in browser `localStorage`.
No server-side session creation — rows are implicitly created on first
`ConversationTurn` insert via upsert.

---

## State Transitions

### Chatbot Request Flow

```
Client sends POST /api/chat
  │
  ├─ Validate input (length ≤ 2000, session_id is UUID)
  │    └─ FAIL → 422 Unprocessable Entity
  │
  ├─ Rate limit check (20 req/min per IP)
  │    └─ EXCEED → 429 Too Many Requests
  │
  ├─ Embed question → OpenAI text-embedding-3-small
  │    └─ FAIL → 503 Service Unavailable
  │
  ├─ Query Qdrant top-5 chunks
  │    └─ EMPTY → answer with "outside scope" label
  │
  ├─ Build prompt with chunks + question
  │
  ├─ Call OpenAI gpt-4o-mini
  │    └─ FAIL → 503 Service Unavailable
  │
  ├─ Persist ConversationTurn to Neon Postgres (non-blocking)
  │    └─ FAIL → log warning, do NOT fail the response
  │
  └─ Return 200 {"answer": str, "session_id": str, "request_id": str}
```

---

## Database Schema (Postgres DDL)

```sql
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE IF NOT EXISTS conversation_turns (
    id            UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id    UUID        NOT NULL,
    question      TEXT        NOT NULL CHECK (char_length(question) <= 2000),
    answer        TEXT        NOT NULL,
    context_chunks JSONB      NOT NULL DEFAULT '[]',
    prompt_tokens  INTEGER    NOT NULL DEFAULT 0,
    completion_tokens INTEGER NOT NULL DEFAULT 0,
    total_tokens   INTEGER    NOT NULL DEFAULT 0,
    model          VARCHAR(50) NOT NULL DEFAULT 'gpt-4o-mini',
    created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_turns_session_created
    ON conversation_turns (session_id, created_at DESC);
```
