---
description: "Task list for Physical AI & Humanoid Robotics Textbook"
---

# Tasks: Physical AI & Humanoid Robotics Interactive Textbook

**Input**: Design documents from `/specs/001-physical-ai-textbook/`
**Prerequisites**: plan.md ✅ spec.md ✅ research.md ✅ data-model.md ✅ contracts/ ✅

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1–US4)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization — Docusaurus site + FastAPI skeleton

- [x] T001 Create Docusaurus 3 project in `textbook/` using `npx create-docusaurus@latest textbook classic --typescript`
- [x] T002 Create FastAPI project skeleton in `chatbot/` with `app/`, `scripts/`, `tests/`, `api/` directories
- [x] T003 [P] Create `chatbot/requirements.txt` with: fastapi, uvicorn, openai, qdrant-client, asyncpg, tiktoken, mangum, slowapi, python-dotenv, pydantic-settings, httpx
- [x] T004 [P] Create `chatbot/.env.example` with all required keys: OPENAI_API_KEY, QDRANT_URL, QDRANT_API_KEY, DATABASE_URL
- [x] T005 [P] Create root `vercel.json` with buildCommand, outputDirectory, Python function config and `/api/*` rewrite rule
- [x] T006 [P] Create `.gitignore` entries for `.env`, `__pycache__`, `node_modules`, `textbook/build`, `.docusaurus`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T007 Create `chatbot/app/config.py` with Pydantic BaseSettings loading OPENAI_API_KEY, QDRANT_URL, QDRANT_API_KEY, DATABASE_URL from environment
- [x] T008 [P] Create `chatbot/app/models.py` with Pydantic schemas: ChatRequest (question: str ≤2000, session_id: UUID), ChatResponse (answer, session_id, request_id, sources), SourceChunk, ErrorResponse
- [x] T009 Create `chatbot/app/main.py` FastAPI app with CORS middleware (whitelist Vercel domain + localhost), X-Request-ID middleware, slowapi rate limiter (20/min per IP), and router inclusion
- [x] T010 Create `chatbot/app/services/db.py` with asyncpg connection pool using DATABASE_URL from config; include `init_db()` coroutine that creates `conversation_turns` table using DDL from data-model.md
- [x] T011 [P] Create `chatbot/scripts/init_db.py` CLI script that calls `init_db()` and prints ✅ confirmation
- [x] T012 Create `chatbot/api/index.py` Vercel Function entry point: import FastAPI app, wrap with `mangum.Mangum(app, lifespan='off')`
- [x] T013 [P] Configure Docusaurus `textbook/docusaurus.config.ts`: set title "Physical AI & Humanoid Robotics", tagline, GitHub URL (sabasohailss45-agenticainewbie/physical-ai-book-saba-sohail), disable blog, set docs as root

**Checkpoint**: Foundation ready — database schema exists, FastAPI starts, Docusaurus builds

---

## Phase 3: User Story 1 — Read & Navigate the Textbook (Priority: P1) 🎯 MVP

**Goal**: Four fully navigable content modules with rich educational content

**Independent Test**: `cd textbook && npm run build` succeeds; open `build/index.html`; all 4 module cards visible; click into any chapter; sidebar shows all chapters in that module

### Implementation for User Story 1

- [x] T014 [P] [US1] Create `textbook/docs/foundations/_category_.json` with label "Module 1: Foundations of Physical AI", position 1
- [x] T015 [P] [US1] Create `textbook/docs/sensing/_category_.json` with label "Module 2: Sensing & Perception", position 2
- [x] T016 [P] [US1] Create `textbook/docs/actuation/_category_.json` with label "Module 3: Actuation & Control", position 3
- [x] T017 [P] [US1] Create `textbook/docs/humanoids/_category_.json` with label "Module 4: Humanoid Robots & Future Directions", position 4
- [x] T018 [P] [US1] Write `textbook/docs/foundations/01-intro.md`: "What is Physical AI?" — definition, history from 1960s robots to modern embodied AI, key milestones table, 3-paragraph theory, real-world examples (Boston Dynamics Spot, Tesla Optimus), summary
- [x] T019 [P] [US1] Write `textbook/docs/foundations/02-embodiment.md`: Embodiment Hypothesis — Rolf Pfeifer's theory, sensorimotor loops, why body shape matters for intelligence, comparison table (software AI vs physical AI), application in robot design, summary
- [x] T020 [P] [US1] Write `textbook/docs/foundations/03-key-systems.md`: Survey of Key Systems — Boston Dynamics Atlas/Spot, Tesla Optimus, Figure 01, Agility Robotics Digit; comparison table (DOF, weight, battery, use case); safety principles (ISO 10218); summary
- [x] T021 [P] [US1] Write `textbook/docs/sensing/01-sensors.md`: Sensor Modalities — cameras (RGB, depth, stereo), LiDAR, IMUs, force/torque, tactile arrays; sensor specs comparison table; strengths/weaknesses; application in humanoid hands; summary
- [x] T022 [P] [US1] Write `textbook/docs/sensing/02-sensor-fusion.md`: Sensor Fusion — Kalman filter intuition, Extended Kalman Filter, particle filters; why fusion > single sensor; SLAM introduction (EKF-SLAM, particle-SLAM); mapping vs localization; practical robotics example; summary
- [x] T023 [P] [US1] Write `textbook/docs/sensing/03-computer-vision.md`: Computer Vision for Robotics — object detection (YOLO family), instance segmentation, 6-DOF pose estimation, optical flow; dataset pipelines for robot training; sim-to-real gap strategies; summary
- [x] T024 [P] [US1] Write `textbook/docs/actuation/01-actuators.md`: Actuator Types — electric (DC, brushless, servo), hydraulic, pneumatic, cable-driven; torque/speed/backdrivability comparison table; why compliance matters for humanoids; SEA vs rigid actuators; summary
- [x] T025 [P] [US1] Write `textbook/docs/actuation/02-kinematics.md`: Kinematics & Dynamics — forward/inverse kinematics, Denavit-Hartenberg parameters, Jacobian matrix (intuitive explanation), workspace analysis, Newton-Euler dynamics, rigid body equations; worked example for 6-DOF arm; summary
- [x] T026 [P] [US1] Write `textbook/docs/actuation/03-control-theory.md`: Control Theory — PID controller (P, I, D terms with intuitive analogies), model-predictive control (MPC), whole-body control overview, reinforcement learning for locomotion (PPO, SAC); sim-to-real for control policies; summary
- [x] T027 [P] [US1] Write `textbook/docs/humanoids/01-humanoid-arch.md`: Humanoid Architecture — mechanical structure (spine, hip, legs, arms, hands), degrees of freedom survey (21–44 DOF), actuation choices per joint, power system design, compute stack (edge GPU, cloud offload); comparison of Atlas, Optimus, Digit; summary
- [x] T028 [P] [US1] Write `textbook/docs/humanoids/02-whole-body-control.md`: Whole-Body Control — loco-manipulation coupling, contact-rich manipulation, task hierarchy (prioritised QP), footstep planning, ZMP criterion, dynamic balancing; case study: stair climbing with arm use; summary
- [x] T029 [P] [US1] Write `textbook/docs/humanoids/03-future-directions.md`: Future Directions — foundation models for robotics (RT-2, RoboFlamingo), world models, dexterous manipulation, social robotics, ethics (job displacement, safety, autonomy levels), regulation landscape, 10-year outlook; summary
- [x] T030 [US1] Create `textbook/src/pages/index.tsx` home page with hero section ("Physical AI & Humanoid Robotics Textbook"), 4 module cards (icon, title, description, "Start Reading" link), and responsive CSS grid layout
- [x] T031 [US1] Update `textbook/sidebars.ts` to auto-generate sidebars from docs folder structure
- [x] T032 [US1] Run `cd textbook && npm run build` and verify zero build errors; fix any MDX syntax issues

**Checkpoint**: All 4 modules live locally — User Story 1 independently testable

---

## Phase 4: User Story 2 — RAG Chatbot (Priority: P2)

**Goal**: Floating chatbot widget on every page, powered by FastAPI RAG backend

**Independent Test**: Start `uvicorn chatbot.app.main:app --port 8000`; POST `/api/chat` with a textbook question; receive non-empty answer within 10 s; verify 429 on 21st request

### Implementation for User Story 2

- [x] T033 [P] [US2] Create `chatbot/app/services/embedder.py`: async function `embed_text(text: str) -> list[float]` using `openai.AsyncOpenAI`, model `text-embedding-3-small`; raise `ServiceUnavailableError` on OpenAI API failure
- [x] T034 [P] [US2] Create `chatbot/app/services/retriever.py`: async function `retrieve_chunks(embedding: list[float], top_k: int = 5) -> list[dict]` using `qdrant_client.AsyncQdrantClient`; query collection `physical-ai-textbook`; return chunk payload list; return empty list on no results
- [x] T035 [P] [US2] Create `chatbot/app/services/generator.py`: async function `generate_answer(question: str, chunks: list[dict]) -> tuple[str, dict]` using `openai.AsyncOpenAI`, model `gpt-4o-mini`; build system prompt with context chunks; if chunks empty use "outside scope" branch; return (answer_text, usage_dict)
- [x] T036 [US2] Create `chatbot/app/routes/chat.py` with: `GET /api/health` returning `{"status":"ok"}`; `POST /api/chat` handler that validates ChatRequest, calls embedder → retriever → generator, persists ConversationTurn to Postgres (non-blocking, swallow DB errors), returns ChatResponse with X-Request-ID header
- [x] T037 [US2] Create `textbook/src/components/ChatWidget/index.tsx`: floating React component (fixed bottom-right, 380×520px panel), input field + send button, message list with user/bot bubbles, session_id from localStorage, calls `fetch('/api/chat')`, loading spinner, error display; TypeScript types for ChatMessage
- [x] T038 [US2] Create `textbook/src/components/ChatWidget/index.module.css` with styles for: floating button, panel open/close animation, message bubbles (user=blue, bot=gray), input bar
- [x] T039 [US2] Swizzle Docusaurus root layout: create `textbook/src/theme/Root.tsx` that wraps children and renders `<ChatWidget />` so it appears on every page
- [x] T040 [US2] Add `OPENAI_API_KEY`, `QDRANT_URL`, `QDRANT_API_KEY`, `DATABASE_URL` to Vercel project environment variables (document in quickstart.md — manual step)
- [x] T041 [US2] Write `chatbot/tests/test_health.py`: test `GET /api/health` returns 200 `{"status":"ok"}` using `httpx.AsyncClient`
- [x] T042 [US2] Write `chatbot/tests/test_chat.py`: test ChatRequest validation (question too long → 422); test rate limit (mock 21 requests → 429); mock OpenAI + Qdrant for happy path test → 200 with answer field

**Checkpoint**: Chatbot answers questions locally — User Story 2 independently testable

---

## Phase 5: User Story 3 — Content Ingestion Pipeline (Priority: P3)

**Goal**: One-command script to chunk, embed, and upsert all textbook content into Qdrant

**Independent Test**: Run `python -m chatbot.scripts.ingest --docs-dir textbook/docs`; check Qdrant dashboard for `physical-ai-textbook` collection; query with a known phrase from Module 1

### Implementation for User Story 3

- [x] T043 [P] [US3] Create `chatbot/scripts/ingest.py`: CLI using argparse with `--docs-dir` argument; walk all `.md` files recursively; extract module_id and chapter_slug from file path; parse Markdown content (strip frontmatter)
- [x] T044 [US3] Add chunking logic to `chatbot/scripts/ingest.py`: use `tiktoken.get_encoding("cl100k_base")`; split text into ≤500-token chunks with 50-token overlap on sentence boundaries; assign deterministic `chunk_id = f"{chapter_slug}_{index}"`
- [x] T045 [US3] Add Qdrant upsert logic to `chatbot/scripts/ingest.py`: create collection `physical-ai-textbook` if not exists (vector_size=1536, distance=Cosine); batch-embed chunks using `embedder.embed_text()`; upsert PointStruct with chunk payload (chunk_id, chapter_slug, module_id, content, token_count); print progress per file
- [x] T046 [US3] Run ingestion against local `textbook/docs/` after Module 1 content is written; verify ≥1 chunk per chapter in Qdrant; fix any chunking edge cases

**Checkpoint**: Qdrant populated — User Story 3 independently testable (chatbot now gives grounded answers)

---

## Phase 6: User Story 4 — Vercel Deployment (Priority: P4)

**Goal**: Public HTTPS URL serving the full textbook + chatbot

**Independent Test**: Visit Vercel URL; home page loads; chatbot widget visible; POST to `/api/chat` returns answer

### Implementation for User Story 4

- [x] T047 [US4] Set up GitHub remote: `git remote add origin https://github.com/sabasohailss45-agenticainewbie/physical-ai-book-saba-sohail.git`
- [x] T048 [US4] Verify `vercel.json` routing: buildCommand points to `cd textbook && npm run build`, outputDirectory is `textbook/build`, Python function entry is `chatbot/api/index.py`, rewrite `/api/(.*)` → `/chatbot/api/index.py`
- [x] T049 [US4] Push branch to GitHub and create Vercel project linked to the repo; set all 4 environment variables in Vercel dashboard
- [x] T050 [US4] Trigger Vercel deployment; monitor build logs; fix any build failures (missing deps, import errors)
- [x] T051 [US4] Validate deployed URL against quickstart.md checklist: health endpoint, home page, module navigation, chatbot response, HTTPS certificate

**Checkpoint**: Hackathon demo URL live — User Story 4 complete

---

## Phase 7: Polish & Cross-Cutting Concerns

- [x] T052 [P] Add structured JSON logging to `chatbot/app/routes/chat.py`: log level, timestamp, latency_ms, status for every request
- [x] T053 [P] Add `chatbot/app/routes/chat.py` error boundary: catch all unhandled exceptions and return `ErrorResponse` with request_id and 500 status
- [x] T054 [P] Update `textbook/src/css/custom.css` with brand colors (dark navy + electric blue) and readable typography (Inter or system font)
- [x] T055 [P] Add `README.md` to repo root with: project description, tech stack badge table, local dev instructions (link to quickstart.md), Vercel deploy button
- [x] T056 Run `pytest chatbot/tests/ -v` and confirm all tests pass
- [x] T057 Run full quickstart.md validation checklist and mark all items ✅

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 completion — **BLOCKS all user stories**
- **US1 — Content (Phase 3)**: Depends on Phase 2; no dependency on US2/US3/US4
- **US2 — Chatbot (Phase 4)**: Depends on Phase 2; independent of US1 content (can mock answers)
- **US3 — Ingestion (Phase 5)**: Depends on Phase 2 + US1 content (needs docs to ingest) + US2 embedder service
- **US4 — Deploy (Phase 6)**: Depends on US1 (content) + US2 (chatbot) + US3 (vectors)
- **Polish (Phase 7)**: Depends on US1–US4 complete

### User Story Dependencies

- **US1 (P1)**: After Foundational — fully independent
- **US2 (P2)**: After Foundational — independent of US1 during build; integrates for full demo
- **US3 (P3)**: After US1 (needs content) + US2 embedder (T033)
- **US4 (P4)**: After US1 + US2 + US3

### Within Each User Story

- Services before routes (T033–T035 before T036)
- Widget before swizzle (T037–T038 before T039)
- Chunking before upsert (T043–T044 before T045)

### Parallel Opportunities

- T014–T029: All 16 content writing tasks are fully parallel (different files)
- T033–T035: embedder, retriever, generator services are parallel (different files)
- T003, T004, T005, T006: Setup files are parallel
- T052–T055: Polish tasks are parallel

---

## Parallel Execution Examples

```bash
# Phase 1 parallel setup (T003, T004, T005, T006 simultaneously):
Task: "Create chatbot/requirements.txt with all deps"
Task: "Create chatbot/.env.example with env var keys"
Task: "Create root vercel.json with routing config"
Task: "Create .gitignore entries"

# Phase 3 content writing (T018–T029 + T014–T017 simultaneously):
Task: "Write foundations/01-intro.md"
Task: "Write foundations/02-embodiment.md"
Task: "Write foundations/03-key-systems.md"
Task: "Write sensing/01-sensors.md"
Task: "Write sensing/02-sensor-fusion.md"
Task: "Write sensing/03-computer-vision.md"
Task: "Write actuation/01-actuators.md"
Task: "Write actuation/02-kinematics.md"
Task: "Write actuation/03-control-theory.md"
Task: "Write humanoids/01-humanoid-arch.md"
Task: "Write humanoids/02-whole-body-control.md"
Task: "Write humanoids/03-future-directions.md"

# Phase 4 service layer (T033, T034, T035 simultaneously):
Task: "Create chatbot/app/services/embedder.py"
Task: "Create chatbot/app/services/retriever.py"
Task: "Create chatbot/app/services/generator.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: US1 (T014–T032)
4. **STOP and VALIDATE**: `npm run build` passes; all 4 modules navigable
5. Deploy static-only to Vercel as checkpoint

### Incremental Delivery

1. Setup + Foundational → skeleton ready
2. US1 (content) → static textbook demo
3. US2 (chatbot backend + widget) → interactive demo
4. US3 (ingestion) → grounded RAG answers
5. US4 (Vercel full deploy) → hackathon submission URL

---

## Notes

- [P] tasks = different files, no blocking dependencies
- Content tasks (T018–T029) are the most time-consuming — start immediately after setup
- All 12 content chapters can be written in parallel by the agent
- Tests (T041, T042, T056) are included per constitution Principle III
- Vercel Python Functions require `mangum` — already in requirements.txt (T003)
- Total tasks: **57** across 7 phases
