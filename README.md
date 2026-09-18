# Link Service

Async URL Shortener Service built with **FastAPI**, **PostgreSQL**, **Redis**, **SQLAlchemy**, and **Alembic**.

## Overview

`link-service` یک سرویس کوتاه‌کننده URL است که برای یادگیری و پیاده‌سازی مفاهیم Backend و AI Systems Engineering طراحی شده است.

سرویس قابلیت‌های زیر را فراهم می‌کند:

* ساخت لینک کوتاه
* دریافت اطلاعات لینک
* Redirect به URL اصلی
* شمارش کلیک‌ها
* Cache با Redis
* Rate Limiting
* Health Check
* Server-Sent Events (SSE)
* مدیریت خطاها
* Logging ساختاریافته
* Async Database Access
* Database Migration با Alembic
* اجرای کامل با Docker Compose
* تست‌های Unit و Integration

---

## Architecture

```text
Client
  │
  ▼
FastAPI
  │
  ├── Middleware
  │     └── Request ID
  │
  ├── Router
  │
  ├── Dependency Injection
  │
  ▼
Service Layer
  │
  ├── Link Service
  ├── Cache Service
  └── Rate Limit Service
  │
  ├───────────────┐
  ▼               ▼
PostgreSQL       Redis
  │               │
  ▼               ▼
SQLAlchemy       Cache
Alembic          Rate Limit
```

---

## Tech Stack

| Technology     | Purpose               |
| -------------- | --------------------- |
| Python 3.12    | Programming Language  |
| FastAPI        | Web Framework         |
| Uvicorn        | ASGI Server           |
| PostgreSQL     | Primary Database      |
| SQLAlchemy     | Async ORM             |
| asyncpg        | PostgreSQL Driver     |
| Redis          | Cache & Rate Limiting |
| Alembic        | Database Migrations   |
| Pydantic       | Validation            |
| Structlog      | Structured Logging    |
| Pytest         | Testing               |
| pytest-asyncio | Async Testing         |
| Ruff           | Linting               |
| Mypy           | Type Checking         |
| Docker         | Containerization      |
| Docker Compose | Local Infrastructure  |
| uv             | Dependency Management |

---

## Project Structure

```text
link-service/
│
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │   ├── deps.py
│   │   └── routes/
│   │       ├── links.py
│   │       ├── health.py
│   │       ├── redirect.py
│   │       ├── events.py
│   │       └── tasks.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── logging.py
│   │   ├── exceptions.py
│   │   └── security.py
│   │
│   ├── db/
│   │   ├── base.py
│   │   └── session.py
│   │
│   ├── models/
│   │   └── link.py
│   │
│   ├── schemas/
│   │   └── link.py
│   │
│   ├── repositories/
│   │   └── link.py
│   │
│   ├── services/
│   │   ├── link.py
│   │   ├── cache.py
│   │   └── rate_limit.py
│   │
│   └── middleware/
│       └── request_id.py
│
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── conftest.py
│
├── scripts/
│   └── start.sh
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
├── pyproject.toml
├── uv.lock
├── .env.example
├── .gitignore
├── .dockerignore
└── README.md
```

---

## Requirements

Before running the project, make sure you have:

* Python 3.12+
* Docker
* Docker Compose
* uv

PostgreSQL and Redis do **not** need to be installed directly on the host machine because they run through Docker Compose.

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd link-service
```

Install dependencies:

```bash
uv sync
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
APP_NAME=Link Service
ENVIRONMENT=development
DEBUG=true

DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/link_service

REDIS_URL=redis://localhost:6379/0

RATE_LIMIT=100
RATE_LIMIT_WINDOW=60
CACHE_TTL=300
```

---

## Start Infrastructure

Start PostgreSQL and Redis:

```bash
docker compose up -d postgres redis
```

Check their status:

```bash
docker compose ps
```

Both services should be healthy.

---

## Database Migration

Run Alembic migrations:

```bash
uv run alembic upgrade head
```

Check the current migration:

```bash
uv run alembic current
```

Show migration history:

```bash
uv run alembic history
```

---

## Run the Application

Start FastAPI:

```bash
uv run uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

## API

### Create Link

```http
POST /links
```

Example request:

```json
{
  "original_url": "https://example.com"
}
```

Example response:

```json
{
  "id": 1,
  "original_url": "https://example.com/",
  "short_code": "F2cjNOv",
  "clicks": 0
}
```

---

### Get Link

```http
GET /links/{link_id}
```

---

### Redirect

```http
GET /r/{short_code}
```

The endpoint resolves the short code and redirects the client to the original URL.

---

### Health Check

```http
GET /health
```

Used to verify that the application is running.

---

## Caching

Redis is used as a cache for frequently accessed links.

The service follows a **cache-aside** pattern:

```text
Request
   │
   ▼
Redis
   │
   ├── Cache Hit ──► Return URL
   │
   └── Cache Miss
          │
          ▼
      PostgreSQL
          │
          ▼
      Store in Redis
          │
          ▼
       Return URL
```

Cache entries use a configurable TTL:

```env
CACHE_TTL=300
```

---

## Rate Limiting

Redis is also used for request rate limiting.

Default configuration:

```env
RATE_LIMIT=100
RATE_LIMIT_WINDOW=60
```

This means a client can make up to 100 requests during a 60-second window.

---

## Testing

Run the complete test suite:

```bash
uv run pytest
```

Run with verbose output:

```bash
uv run pytest -v
```

Run only unit tests:

```bash
uv run pytest tests/unit
```

Run only integration tests:

```bash
uv run pytest tests/integration
```

---

## Code Quality

Run Ruff:

```bash
uv run ruff check .
```

Run Mypy:

```bash
uv run mypy app
```

Run pre-commit:

```bash
uv run pre-commit run --all-files
```

---

## Docker

Build the application image:

```bash
docker compose build
```

Start the complete stack:

```bash
docker compose up
```

Run in detached mode:

```bash
docker compose up -d
```

Check services:

```bash
docker compose ps
```

View logs:

```bash
docker compose logs -f
```

Stop services:

```bash
docker compose down
```

---

## Database

The project uses PostgreSQL as the primary persistent storage.

The `links` table contains:

```text
id
original_url
short_code
clicks
created_at
```

Database schema changes are managed through Alembic.

Never modify the production database schema manually when a migration should be used.

---

## Error Handling

The application uses a custom exception hierarchy:

```text
LinkServiceError
├── LinkNotFoundError
├── LinkCreationError
├── RateLimitExceededError
└── CacheError
```

This keeps domain errors separate from infrastructure errors.

---

## Logging

The project uses `structlog` for structured logging.

Example:

```text
application_started
application_shutdown_started
application_stopped
```

Request IDs are also added through middleware to make request tracing easier.

---

## Application Lifecycle

FastAPI lifespan is used to manage application startup and shutdown.

Startup:

```text
Application Start
      │
      ▼
Configure Logging
      │
      ▼
Connect to Redis
      │
      ▼
Redis Ping
      │
      ▼
Application Ready
```

Shutdown:

```text
Application Shutdown
      │
      ▼
Close Redis
      │
      ▼
Release Resources
      │
      ▼
Application Stopped
```

---

## Development Workflow

Typical development workflow:

```bash
uv sync

docker compose up -d postgres redis

uv run alembic upgrade head

uv run pytest

uv run uvicorn app.main:app --reload
```

Before committing:

```bash
uv run ruff check .
uv run mypy app
uv run pytest
```

---

## Learning Goals

This project is designed to practice:

* Python type hints
* Async programming
* FastAPI
* Dependency Injection
* Middleware
* Lifespan
* Background Tasks
* SQLAlchemy Async
* PostgreSQL
* Redis
* Cache-aside
* Rate Limiting
* Alembic
* Repository Pattern
* Service Layer
* Exception Handling
* Structured Logging
* Testing
* Docker
* CI/CD
* Git
* Production-oriented backend architecture

---

## Status

The project is being developed incrementally as part of an intensive AI Engineering / Backend Engineering learning path.

Current architecture includes:

* FastAPI
* PostgreSQL
* Redis
* SQLAlchemy
* Alembic
* Async services
* Caching
* Rate limiting
* Testing
* Docker
* Structured logging
* Request ID middleware
* Health checks
* SSE
* CI configuration
