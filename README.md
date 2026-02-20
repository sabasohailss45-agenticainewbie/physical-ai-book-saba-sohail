# Physical AI & Humanoid Robotics Textbook

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/sabasohailss45-agenticainewbie/physical-ai-book-saba-sohail)

An interactive open-source textbook on Physical AI and Humanoid Robotics, featuring an embedded RAG-powered AI tutor.

## Tech Stack

| Layer | Technology |
|---|---|
| Documentation site | Docusaurus 3 (React + TypeScript) |
| AI Tutor Backend | FastAPI (Python 3.11) |
| Vector Store | Qdrant Cloud |
| Conversation DB | Neon Postgres (serverless) |
| LLM | OpenAI GPT-4o-mini |
| Embeddings | OpenAI text-embedding-3-small |
| Deployment | Vercel |

## Textbook Modules

1. **Foundations of Physical AI** — definitions, embodiment, key systems
2. **Sensing & Perception** — sensors, sensor fusion, SLAM, computer vision
3. **Actuation & Control** — actuators, kinematics, dynamics, PID, RL
4. **Humanoid Robots & Future Directions** — architecture, WBC, foundation models, ethics

## Local Development

See [specs/001-physical-ai-textbook/quickstart.md](specs/001-physical-ai-textbook/quickstart.md) for full instructions.

### Quick start

```bash
# 1. Install deps
cd textbook && npm install && cd ..
cd chatbot && pip install -r requirements.txt && cd ..

# 2. Configure env
cp chatbot/.env.example chatbot/.env
# Edit chatbot/.env with your API keys

# 3. Init DB
cd chatbot && python -m scripts.init_db

# 4. Ingest content
python -m scripts.ingest --docs-dir ../textbook/docs

# 5. Start backend
uvicorn app.main:app --reload --port 8000

# 6. Start frontend (new terminal)
cd textbook && npm run start
```

Visit `http://localhost:3000` — click the 🤖 button to chat.

## Deploy to Vercel

1. Push to GitHub
2. Import repo in [Vercel](https://vercel.com)
3. Set environment variables: `OPENAI_API_KEY`, `QDRANT_URL`, `QDRANT_API_KEY`, `DATABASE_URL`
4. Deploy

## License

MIT
