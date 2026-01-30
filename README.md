# FastAPI Microservice — Voice AI Orchestration (Evaluation Task)

This project implements a high-performance, asynchronous microservice for ingesting real-time call metadata, orchestrating AI transcription and sentiment analysis, and reliably handling flaky external AI dependencies.

The system is designed to handle **high concurrency**, **non-blocking ingestion**, **fault tolerance**, and **race conditions**, following production-grade backend engineering principles.

---

## 🚀 Key Features

* **Async Non-Blocking Ingestion**

  * Handles thousands of concurrent requests.
  * Guarantees API response < 50ms.
  * Validates packet sequence ordering.

* **State Machine Based Call Processing**

  * Deterministic transitions:

    * `IN_PROGRESS → COMPLETED → PROCESSING_AI → ARCHIVED`
    * Failure handling with retry → `FAILED`

* **Fault-Tolerant AI Orchestration**

  * Simulates flaky external AI APIs.
  * 25% failure rate.
  * Exponential backoff retry strategy.

* **Concurrency Safe**

  * Database row-level locking to prevent race conditions.

* **Real-Time Updates via WebSockets**

  * Live supervisor dashboard feed.

* **Full Integration Testing**

  * Covers concurrency & race conditions.

---

## 🏗️ System Architecture

```
                   ┌──────────────┐
Incoming Requests ─▶  FastAPI API  │
                   └───────┬──────┘
                           │
                           ▼
                  Async PostgreSQL
                           │
                           ▼
                  Background Workers
                           │
                           ▼
                 Flaky AI Simulation
                           │
                           ▼
                    WebSocket Feed
```

---

## 🔁 Call Processing Flow

```
IN_PROGRESS
     ↓
COMPLETED
     ↓
PROCESSING_AI
     ↓
ARCHIVED

Failure → Retry → FAILED (after max attempts)
```

---

## 🛠 Tech Stack

* **Backend:** FastAPI (Async)
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy Async
* **Concurrency:** asyncio
* **Retries:** tenacity
* **Testing:** pytest, httpx.AsyncClient
* **WebSockets:** FastAPI WebSocket

---

## 📦 Project Structure

```
app/
 ├── main.py          # Application entrypoint
 ├── db.py            # Async DB setup
 ├── models.py        # Database models
 ├── schemas.py       # Pydantic schemas
 ├── workers.py       # Background AI orchestration
 ├── ai_mock.py       # Flaky AI simulation
 └── websocket.py     # Real-time dashboard updates

tests/
 └── test_race.py     # Integration tests

README.md
docker-compose.yml
```

---

## ⚙️ Setup Instructions

### 1. Clone Repository

```bash
git clone https://github.com/<your-username>/fastapi-voice-ai-microservice.git
cd fastapi-voice-ai-microservice
```

### 2. Setup Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Start PostgreSQL (Docker Recommended)

```bash
docker compose up -d
```

### 5. Run Application

```bash
uvicorn app.main:app --reload
```

API available at:

```
http://localhost:8000
```

Swagger UI:

```
http://localhost:8000/docs
```

---

## 🔌 API Endpoints

### Packet Ingestion

```
POST /v1/call/stream/{call_id}
```

Payload:

```json
{
  "sequence": 1,
  "data": "base64_encoded_audio_chunk",
  "timestamp": 1738173341.123
}
```

Returns:

```
202 Accepted
```

---

### WebSocket — Supervisor Dashboard

```
/ws/supervisor
```

Streams live call state updates.

---

## 🧪 Running Tests

```bash
pytest
```

Includes **integration tests simulating race conditions** and **concurrent packet arrival**.

---

## 🧠 Methodology

### Design Principles

* **Asynchronous everywhere** — zero blocking operations.
* **Stateless API + Stateful DB** — reliable persistence.
* **Retry-first design** — resilience to flaky AI APIs.
* **Concurrency-safe writes** — row-level DB locking.

### Race Condition Handling

Simultaneous requests for the same `call_id` are synchronized using **database row locking (`SELECT FOR UPDATE`)**, ensuring correct packet ordering and consistency.

---

## 📈 Performance Goals

* API response time: **< 50ms**
* Supports **thousands of concurrent streams**
* Handles **bursty traffic without backpressure**

---

## 📌 Future Improvements

* Redis-based distributed task queue
* Real AI transcription integration
* Dashboard frontend UI
* Horizontal scaling using Kubernetes

---

## 👨‍💻 Author

**Chandan Agarwal**
Backend & Systems Engineer
