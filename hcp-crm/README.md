# AI First CRM — HCP Interaction Module

An AI-powered CRM for medical representatives to log interactions with Healthcare
Professionals (HCPs) via a structured form **or** a conversational AI chat that
extracts entities (doctor, hospital, products, priority, follow-up date) and
saves them automatically.

> **Scope note:** This is a complete, runnable full-stack foundation — auth,
> HCP/interaction CRUD, dashboard, analytics, and a LangGraph-based AI chat
> agent with 5 tools — built cleanly so every module can be extended. It does
> not include every bonus item from the original brief (OCR prescription
> reading, speech-to-text, PDF/Excel export, calendar sync); those are noted
> as TODOs below rather than faked.

---

## Tech Stack

**Frontend:** React 19, Vite, Redux Toolkit, React Router DOM, Material UI,
React Hook Form, Axios, Framer Motion, React Icons, Recharts, Inter + Fraunces fonts.

**Backend:** FastAPI, SQLAlchemy, Pydantic, Alembic, JWT auth, LangGraph,
LangChain, Groq API (Gemma2-9B-IT), PostgreSQL, Redis (optional), Docker.

---

## Folder Structure

```
hcp-crm/
├── backend/
│   ├── app/
│   │   ├── core/          # config, security, auth deps
│   │   ├── db/            # SQLAlchemy engine/session
│   │   ├── models/        # Users, Doctors, Hospitals, Products, Interactions,
│   │   │                    Followups, Notifications, AuditLogs
│   │   ├── schemas/       # Pydantic request/response models
│   │   ├── api/routes/    # auth, doctors, interactions, chat, dashboard, ...
│   │   ├── agent/         # LangGraph agent (graph.py) + rule-based fallback
│   │   └── main.py
│   ├── alembic/           # migrations
│   ├── seed.py            # demo data
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/           # axios client + endpoint wrappers
│   │   ├── store/slices/  # auth, doctor, interaction, chat, dashboard, theme, notification
│   │   ├── components/    # Navbar, Sidebar, forms, tables, charts, chat UI, primitives
│   │   ├── pages/         # Login, Dashboard, Doctors, DoctorProfile, LogInteraction,
│   │   │                    AIChat, InteractionHistory, Analytics, Notifications,
│   │   │                    Profile, Settings, NotFound
│   │   └── theme/         # design tokens + MUI theme
├── docker-compose.yml
└── .github/workflows/ci.yml
```

---

## Installation

### Prerequisites
- Python 3.11+
- Node.js 20+
- Docker Desktop

### 1. Environment variables

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

Edit `backend/.env`:
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ai_crm
SECRET_KEY=replace-with-a-long-random-string
GROQ_API_KEY=your_groq_api_key_here   # optional — see "Groq API Setup" below
GROQ_MODEL=gemma2-9b-it
```

### 2. Run Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python seed.py          # creates demo admin user + sample doctor
uvicorn app.main:app --reload --port 8000
```

API docs available at `http://localhost:8000/docs`.

Demo login: `admin@hcpcrm.com` / `Admin@123`

### 3. Run Frontend

```bash
cd frontend
npm install
npm run dev
```

App available at `http://localhost:5173`.

### 4. Database Migrations (production)

`app.main` auto-creates tables on startup for convenience in dev. For
production, use Alembic instead:

```bash
cd backend
alembic revision --autogenerate -m "init"
alembic upgrade head
```

### 5. Docker Database

```bash
docker compose up -d
```
Backend: `:8000` · Frontend: `:5173` · Postgres: `:5432` · Redis: `:6379`

---

## PostgreSQL Docker Setup

PostgreSQL runs only through Docker Compose. Do not install PostgreSQL locally.

### Start Database

```bash
docker compose up -d
```

### Check Running Containers

```bash
docker ps
```

### Check Database Logs

```bash
docker logs ai-crm-postgres
```

### Run Backend

```bash
cd backend
python -m venv .venv
```

Windows

```bash
.venv\Scripts\activate
```

Linux

```bash
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

On successful startup, the backend prints:

```bash
✅ PostgreSQL Connected Successfully
```

## Groq API Setup

1. Create a key at https://console.groq.com
2. Set `GROQ_API_KEY` and `GROQ_MODEL=gemma2-9b-it` in `backend/.env`.
3. Without a key, the AI Chat still works — `app/agent/extractor.py` provides
   a regex-based fallback for entity extraction so the app runs end-to-end
   out of the box.

---

## LangGraph Agent Flow

```
classify_intent
   ├─ log_interaction   -> extract entities, summarize, persist Interaction
   ├─ search_hcp        -> look up doctor/hospital
   ├─ summarize         -> summarize free text + sentiment/products
   ├─ schedule_followup -> derive follow-up date + priority
   ├─ edit_interaction  -> identify fields to update
   └─ general_chat      -> conversational fallback (Groq if configured)
        │
        ▼
     respond -> END
```

Defined in `backend/app/agent/graph.py`. State (`AgentState`) carries the
message, detected intent, extracted entities, and tool result between nodes.

---

## API Endpoints

| Method | Path | Description |
|---|---|---|
| POST | `/api/auth/register` | Create a user |
| POST | `/api/auth/login-json` | Login (JSON, used by frontend) |
| GET | `/api/dashboard` | Dashboard stats + activity |
| GET | `/api/analytics` | Priority/specialization breakdowns |
| GET/POST | `/api/doctors`, `/api/doctor` | List / create doctor |
| PUT/DELETE | `/api/doctor/{id}` | Update / delete doctor |
| GET/POST | `/api/interaction` | List / create interaction |
| PUT/DELETE | `/api/interaction/{id}` | Update / delete interaction |
| POST | `/api/chat` | AI chat (LangGraph agent) |
| GET | `/api/notifications` | List notifications |

Full interactive spec at `/docs` (Swagger UI).

---

## Known TODOs / Not Included

- OCR prescription reader, speech-to-text
- PDF/Excel export, generated email drafts
- Calendar sync for follow-ups
- Infinite scroll (tables use server-side pagination instead)
- Full Redis caching layer (Redis is wired up but unused by default)

---

## Deployment

- **Backend:** containerized via `backend/Dockerfile`; deploy to any
  container host (Render, Railway, ECS, etc.) with `DATABASE_URL` pointing
  at a managed Postgres instance.
- **Frontend:** `frontend/Dockerfile` builds a static bundle served by nginx;
  alternatively deploy the `dist/` output to Vercel/Netlify with
  `VITE_API_BASE_URL` set to your backend's public URL.
