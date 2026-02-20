# Feature Specification: Physical AI & Humanoid Robotics Interactive Textbook

**Feature Branch**: `001-physical-ai-textbook`
**Created**: 2026-02-21
**Status**: Draft

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Read & Navigate the Textbook (Priority: P1)

A student or professional visits the site, browses the four learning modules,
and reads structured content about Physical AI and humanoid robotics with clear
progression from fundamentals to advanced applications.

**Why this priority**: The textbook content is the entire product — without it,
nothing else delivers value.

**Independent Test**: Navigate to any module page; verify the chapter heading,
body text, and code/diagram blocks render correctly without the chatbot.

**Acceptance Scenarios**:

1. **Given** a visitor lands on the home page, **When** they click a module card,
   **Then** they see a chapter page with title, section headings, body paragraphs,
   and any embedded figures or code snippets.
2. **Given** a reader is on a chapter page, **When** they use the sidebar,
   **Then** they can jump to any other chapter within 1 click.
3. **Given** a mobile user visits the site, **When** the page loads,
   **Then** the layout is fully responsive and all text is legible without horizontal scroll.

---

### User Story 2 — Ask the RAG Chatbot (Priority: P2)

A reader types a question into the embedded chatbot and receives a concise,
grounded answer that cites content from the textbook modules.

**Why this priority**: The chatbot is the interactive differentiator that
separates this textbook from a static site.

**Independent Test**: Open the chatbot widget, type "What is a humanoid robot?",
and verify a non-empty, relevant answer is returned within 10 seconds.

**Acceptance Scenarios**:

1. **Given** the chatbot widget is open, **When** a user submits a question,
   **Then** the chatbot returns an answer grounded in textbook content within 10 s.
2. **Given** a user asks a question outside the textbook scope,
   **When** the system cannot find relevant context,
   **Then** the chatbot responds politely that the topic is not covered.
3. **Given** the user sends more than 2000 characters,
   **When** the request reaches the backend,
   **Then** the system returns a validation error and does not call the LLM.
4. **Given** a user submits 20+ requests per minute,
   **When** the rate limit is exceeded,
   **Then** the server returns a 429 response with a retry-after hint.

---

### User Story 3 — Content Ingestion Pipeline (Priority: P3)

A maintainer runs a one-command ingestion script that chunks all textbook
Markdown files, generates embeddings, and upserts them into the Qdrant
collection so the RAG chatbot can answer questions.

**Why this priority**: Without ingested embeddings the chatbot cannot answer;
this is a developer concern not visible to end readers.

**Independent Test**: Run the ingestion command, then query Qdrant for a known
phrase from Module 1; verify at least one matching vector is returned.

**Acceptance Scenarios**:

1. **Given** textbook Markdown files exist, **When** the ingestion script runs,
   **Then** all files are chunked, embedded, and upserted with zero errors.
2. **Given** a file has already been ingested, **When** the script runs again,
   **Then** vectors are upserted (not duplicated) using deterministic chunk IDs.

---

### User Story 4 — Deploy to Vercel (Priority: P4)

The entire project (Docusaurus site + FastAPI chatbot backend) is deployed to
Vercel and accessible via a public URL with HTTPS.

**Why this priority**: Deployment is required for the hackathon demo but all
other stories can be validated locally first.

**Independent Test**: Visit the Vercel deployment URL; verify the home page
loads and the chatbot returns a response.

**Acceptance Scenarios**:

1. **Given** the repo is pushed to GitHub, **When** Vercel deploys,
   **Then** the public URL serves the Docusaurus site with HTTPS.
2. **Given** the Vercel deployment is live, **When** the chatbot widget sends
   a question, **Then** the FastAPI backend responds correctly.

---

### Edge Cases

- What happens when the OpenAI API is unavailable? → Chatbot returns a
  503 with a user-friendly "Service temporarily unavailable" message.
- What happens when Qdrant returns no results? → Chatbot answers with a
  polite "Outside textbook scope" label rather than hallucinating.
- What if a Markdown file is malformed during ingestion? → The script logs
  an error for that file and continues processing the remaining files.
- What if Neon Postgres is unreachable? → Session history is skipped
  gracefully; stateless conversation still works.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST serve a Docusaurus 3 site with four content modules:
  (1) Foundations of Physical AI, (2) Sensing & Perception,
  (3) Actuation & Control, (4) Humanoid Robots & Future Directions.
- **FR-002**: Each module MUST contain at least 3 chapters with: introduction,
  theory section, real-world application section, and summary.
- **FR-003**: Site MUST include a persistent chatbot widget accessible from
  every page without requiring a page reload.
- **FR-004**: Chatbot widget MUST communicate with a FastAPI backend via
  `POST /api/chat` with JSON body `{"question": str, "session_id": str}`.
- **FR-005**: Backend MUST retrieve the top-5 most relevant text chunks from
  the vector store and include them as context in the LLM prompt.
- **FR-006**: Backend MUST store each conversation turn (question + answer) in
  a relational database with session_id, timestamp, and token usage.
- **FR-007**: Backend MUST expose `GET /api/health` returning `{"status":"ok"}`.
- **FR-008**: Ingestion script MUST chunk Markdown files into ≤500-token
  segments with 50-token overlap and upsert to the vector collection.
- **FR-009**: All secrets MUST be loaded from environment variables; none
  committed to version control.
- **FR-010**: Deployment configuration MUST serve the static site at the root
  and proxy `/api/*` requests to the FastAPI backend.

### Key Entities

- **Module**: A top-level textbook section (id, title, slug, chapter list).
- **Chapter**: A single Markdown page (id, module_id, title, slug, content).
- **Chunk**: A vector-indexed text fragment (chunk_id, chapter_slug,
  content, token_count).
- **ConversationTurn**: A persisted chat exchange (id, session_id, question,
  answer, context_chunks JSON, token_usage, created_at).
- **Session**: A browser-side session identifier (UUID v4, stored in
  localStorage).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All four modules are live and navigable on the public URL within
  the hackathon deadline.
- **SC-002**: Chatbot returns a relevant answer to a textbook question in under
  10 seconds end-to-end (local and deployed).
- **SC-003**: Ingestion pipeline processes all textbook chapters with zero
  uncaught exceptions.
- **SC-004**: The public deployment URL is accessible via HTTPS.
- **SC-005**: Chatbot correctly declines with a polite message for at least
  one out-of-scope question during the demo.
- **SC-006**: Rate limiting prevents more than 20 chatbot requests per minute
  from the same origin.

## Assumptions

- No user authentication is required for this hackathon scope.
- Session IDs are generated client-side (UUID v4) and stored in localStorage.
- OpenAI embeddings and chat models are used (cost-optimised variants).
- Cloud-hosted vector store and serverless relational DB free tiers are
  sufficient for hackathon traffic.
- Vercel hobby plan is sufficient for deployment.
