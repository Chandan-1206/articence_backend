# FastAPI Backend Intern Evaluation — Call Processing Service

This repository contains an asynchronous FastAPI microservice built as part of a backend evaluation task.  
The service ingests streaming call metadata, manages call lifecycle state, orchestrates flaky AI processing with retries, and safely handles concurrency and race conditions.

The focus of this project is **backend correctness, async design, and reliability**, not real AI or frontend UI.

---

## ✅ Implemented Requirements

### 1. Async, Non-Blocking Ingestion
- `POST /v1/call/stream/{call_id}`
- Accepts streaming metadata packets
- Returns **202 Accepted** immediately
- Detects out-of-order packets and logs warnings
- Never blocks request handling

---

### 2. Call State Machine (Persistent)
Each call is stored in PostgreSQL and transitions through deterministic states:
```bash
IN_PROGRESS → COMPLETED → PROCESSING_AI → ARCHIVED
↓
FAILED
```
State is the single source of truth for orchestration and idempotency.

---

### 3. PostgreSQL + Async SQLAlchemy
- Async engine (`asyncpg`)
- Persistent call and packet storage
- Safe concurrent writes
- No in-memory state assumptions

---

### 4. Flaky AI Simulation
- Simulates an unreliable external AI dependency
- Random latency (1–3 seconds)
- Configurable failure rate (default 25%)
- No real AI APIs used

---

### 5. Retry with Exponential Backoff
- Automatic retries on AI failure
- Backoff strategy: `1s → 2s → 4s`
- Max retry attempts enforced
- Final failure transitions call to `FAILED`

---

### 6. Concurrency & Race Condition Safety
- Concurrent packet ingestion supported
- Safe call creation under concurrent requests
- Primary-key conflicts handled explicitly
- Idempotent completion logic prevents duplicate background jobs

---

### 7. Integration Testing
- Async integration test using `pytest` + `httpx`
- Simulates concurrent packet ingestion
- Verifies race-condition safety
- Uses real database behavior (not mocks)

---

### 8. (Optional) WebSocket Supervisor Updates
- WebSocket endpoint for supervisors:
   `/ws/supervisor`
- Emits updates on **call state transitions only**
- Demonstrates event-driven, real-time backend design
- Optional, non-blocking, no polling

---

## 🧠 Design Decisions (Intentional)

- **No Celery / Redis** — out of scope for evaluation
- **No real AI** — focus is orchestration, not ML
- **No Docker required** — local PostgreSQL is sufficient
- **No auth / frontend** — not part of task
- **Async everywhere** — DB, API, background workflows

---

## 🛠 Tech Stack

- FastAPI
- Uvicorn (WebSocket enabled)
- PostgreSQL
- SQLAlchemy (Async)
- asyncpg
- pytest + httpx
- Python asyncio

---

## 📦 Project Structure
```bash

articence_backend/
├── app/
│   ├── __init__.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── calls.py
│   │   └── ws.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── flaky_ai.py
│   ├── create_tables.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
│
├── tests/
│   ├── __init__.py
│   ├── test_dbconn.py
│   └── test_race_condition.py
│
├── .env.example
├── .gitignore
├── requirements.txt
├── dev-requirements.txt
└── run.py

```

---

## ⚙️ Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure environment
Create .env:
`DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/articence_db`

### 3. Run the service
`python run.py`
- Server:
  `http://127.0.0.1:8000`
- Swagger:
  `http://127.0.0.1:8000/docs`

---

## 🔌 API Overview

### Stream packet
`POST /v1/call/stream/{call_id}`

json
```bash
{
  "sequence": 1,
  "data": "audio_chunk",
  "timestamp": 1.23
}
```
Returns:
`202 Accepted`

### Complete call
`POST /v1/call/complete/{call_id}`
Triggers AI orchestration (once, idempotent).

### WebSocket
`ws://127.0.0.1:8000/ws/supervisor`
Recieves live call state updates.

---

## 🧪 Run Tests
```bash
pip install -r dev-requirements.txt
pytest
```
---

## 📌 What This Project Demonstrates
- Async backend engineering
- State-driven orchestration
- Fault tolerance
- Retry strategies
- Race-condition handling
- Clean separation of concerns
- Production-style decision making

---

## 👤 Author
Chandan Agarwal
Backend Engineering Candidate
