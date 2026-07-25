# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

This repo is a job-assessment deliverable (Bangkok Bank AI Engineer — Agentic AI test): a two-agent RAG system built with LangGraph. Full design rationale, architecture diagram, and sequence diagram live in `PLAN.md` — read it before making structural changes, since several implementation choices there are deliberate trade-offs (not defaults) explained with reasoning.

**Status:** design-phase. Only `PLAN.md` and `knowledge_base.txt` (15 paragraph chunks) exist so far. Remaining files are written in this order: `config.py` → `models/schemas.py` → `services/vector_store.py` → `services/retriever_tool.py` → `services/agents.py` → `main.py`.

## Commands

No `requirements.txt` exists yet. Once created per `PLAN.md`, the dependency set is: `langgraph`, `langchain-anthropic`, `chromadb`, `sentence-transformers`, `python-dotenv`.

```bash
pip install -r requirements.txt
python main.py          # runs the sample queries end-to-end; auto-builds the Chroma index on first run if chroma_db/ is missing
```

`ANTHROPIC_API_KEY` must be set (via `.env`, copied from `.env.example`).

## Architecture

Two LangGraph nodes wired sequentially in a `StateGraph`, sharing one state object defined in `models/schemas.py` (`GraphState`: `query`, `snippets`, `final_answer`):

1. **Data Retriever node** — calls a single custom tool, `search_knowledge_base(query) -> list[str]`, defined in `services/retriever_tool.py`. The tool embeds the query with `sentence-transformers` (`all-MiniLM-L6-v2`) and queries ChromaDB for the closest chunks. It returns **raw snippets only** — it must never synthesize or answer the question itself.
2. **Report Generator node** — takes the snippets from state and calls Claude (via `langchain-anthropic`, model `claude-haiku-4-5`) to synthesize one non-redundant, formatted answer. It has no tools.

`services/vector_store.py` owns index construction: it reads `knowledge_base.txt`, chunks it, embeds each chunk, and persists to `chroma_db/`. This runs once (idempotent — skipped if `chroma_db/` already exists), not per query. `config.py` centralizes all constants (`ANTHROPIC_API_KEY`, `CLAUDE_MODEL`, `EMBEDDING_MODEL`, `CHROMA_DIR`, `KNOWLEDGE_BASE_PATH`, `TOP_K`) — no other file should hardcode these.

### Folder layout rationale (see `PLAN.md` for full discussion)

- `services/` holds all business logic (vector store, tool, agent/graph), separate from `main.py`.
- `models/schemas.py` follows the same folder/file convention as the reference project `../Ai-Rag-Chat` (`models/` is the folder name; `schemas.py` is a file inside it, not a separate "schema folder"). It holds only the LangGraph state shape — there is no database-backed model.
- No `routers/` — there is no HTTP layer; this is a script, not a web service, so nothing needs an API-routing layer.
- No ORM / database `models` (e.g. `class User(Base)`) — the only persistent store is ChromaDB (a vector database), accessed via its client library directly, not through an ORM.
- `knowledge_base.txt` stays at the repo root rather than under a `data/` folder, since the assignment names this exact file as a required deliverable.

### Key non-obvious design decisions (see `PLAN.md` for full rationale)

- **Chunking is paragraph-based** (`text.split("\n\n")`), not fixed-character-count. `knowledge_base.txt` content is Thai, which has no inter-word spaces — character-count chunking risks splitting mid-word and corrupting embeddings. Every knowledge-base entry must therefore be separated by a blank line.
- **Chunk granularity is one fact per chunk** (15 chunks total: 1 overview + 14 specific policy facts), not one chunk per broad topic. A broad topic-per-chunk design was tried first and rejected — it caused imprecise retrieval (a narrow question like "sick leave days" would pull in unrelated facts bundled in the same paragraph). The first chunk is a deliberate overview/summary paragraph so broad questions ("what policies exist?") still retrieve a coherent answer even though every other chunk is narrow.
- **The retriever tool is not exposed for the agent to "choose"** — the assignment only requires one tool, always invoked, so the Data Retriever node calls it directly rather than routing through LLM tool-selection.
- **LangGraph was chosen over a plain LangChain LCEL chain** even though the workflow has no branches or loops — it was picked to make the multi-agent handoff explicit in code, matching the assessment's evaluation criteria, not because the linear flow requires graph semantics.
- **ChromaDB + sentence-transformers were chosen over a from-scratch TF-IDF implementation** — a deliberate trade-off favoring the author's prior familiarity with the embed-and-store pattern over a dependency-free approach, explicitly checked for compliance against the assignment text (which only requires "keyword or basic semantic search," not a specific technique).

## Knowledge base content

`knowledge_base.txt` is Thai-language company policy, 15 blank-line-separated chunks: 1 overview paragraph, then leave policy (sick/personal/annual/maternity — adapted from `../Ai-Rag-Chat/data/sample.txt`), working hours & overtime, international travel policy, and expense reimbursement policy — each individual fact as its own chunk.
