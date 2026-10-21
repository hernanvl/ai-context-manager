# AI Context Manager for Long Conversations

A lightweight RAG-based memory system that preserves important information from long AI conversations, compresses it into structured **Context Packs**, and injects relevant context into new chats so long-term projects never lose continuity.

## Features
- **Conversation storage**: projects -> chats -> messages in PostgreSQL
- **Automatic context compression**: structured summaries (goals, decisions, facts, constraints, open tasks, technical notes)
- **Versioned Context Packs**: reusable project state, exportable as Markdown
- **Semantic retrieval**: pgvector similarity search over messages and summaries
- **Context injection**: relevant pack + snippets added to the system prompt before every LLM call

## Architecture
```
Next.js UI  ->  FastAPI  ->  Groq LLM
                   |
                   +-> sentence-transformers (embeddings)
                   +-> Supabase Postgres + pgvector
```

## Tech stack
| Layer | Tool |
|---|---|
| Frontend | Next.js, Tailwind CSS, shadcn/ui |
| Backend | FastAPI (Python) |
| LLM | Groq API (free tier) |
| Embeddings | sentence-transformers `all-MiniLM-L6-v2` (local, 384-dim) |
| Database | Supabase PostgreSQL + pgvector |
| Auth | Supabase Auth |

## Project structure
```
backend/    FastAPI app (routers, services)
frontend/   Next.js app
supabase/   SQL schema and migrations
docs/       Architecture notes and assets
```

## Roadmap
- [x] Phase 1: Database schema
- [ ] Phase 2: Chat endpoint + message storage
- [ ] Phase 3: Embeddings + similarity search
- [ ] Phase 4: Auto-summarization + Context Packs
- [ ] Phase 5: Context injection
- [ ] Phase 6: Next.js dashboard
- [ ] Phase 7: Evaluation, demo, docs

## Setup
1. Copy `.env.example` to `.env` and fill in your keys.
2. In Supabase SQL Editor, run `supabase/schema.sql`.
3. Backend: see `backend/README.md` (coming in Phase 2).
