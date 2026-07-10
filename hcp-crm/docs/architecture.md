# Architecture Overview

## High-level flow

```
React (Vite) SPA
   │  axios (JWT bearer)
   ▼
FastAPI backend
   ├── /api/auth        → JWT issuance
   ├── /api/doctor(s)   → HCP CRUD
   ├── /api/interaction → interaction CRUD
   ├── /api/chat        → LangGraph agent
   │        │
   │        ├── classify_intent
   │        ├── log_interaction / search_hcp / summarize /
   │        │   schedule_followup / edit_interaction tools
   │        └── general_chat (Groq Gemma2-9B-IT, optional)
   ├── /api/dashboard   → aggregated stats
   └── /api/analytics   → priority/specialization breakdowns
   │
   ▼
PostgreSQL (SQLAlchemy models: Users, Doctors, Hospitals, Products,
             Interactions, Followups, Notifications, AuditLogs)
```

## Auth
JWT bearer tokens issued on login, verified per-request via a FastAPI
dependency (`app/core/deps.py`). Role field on `User` (`admin`, `manager`,
`medical_rep`) supports RBAC via `require_role(...)`.

## AI Chat
`app/agent/graph.py` builds a LangGraph `StateGraph` with a
`classify_intent` entry node that routes to one of five tools, each of
which mutates shared `AgentState` before a shared `respond` node composes
the reply. When `GROQ_API_KEY` is unset, extraction falls back to
`app/agent/extractor.py`'s regex-based logic so the whole app is runnable
without external API access.
