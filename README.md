# Enterprise RAG Knowledge Base Agent

Academic Core MVP based on the supplied Proposal V5.1. Stack: Django/DRF, React, PostgreSQL + pgvector, Redis, Celery, Docker.

## Features in this MVP
- Token authentication and tenant membership / role checks
- Tenant-scoped document upload, processing status, chunking and indexing
- PDF, DOCX and TXT extraction
- OpenAI embeddings and GPT-4o-mini generation (optional; safe abstention when no API key)
- PostgreSQL full-text search + pgvector similarity retrieval, fused hybrid ranking
- Cited answers with citation-marker validation, chat history, feedback, basic audit records
- Admin Django interface, React workspace, Docker Compose, health endpoint and tests

> This is a working academic MVP foundation, not a certified production deployment. SSO/OIDC, connector framework, object storage, advanced reranking, ticket actions, formal evaluation UI, OpenTelemetry and full Phase 2 capabilities remain extension work.

## Quick start (Docker)
1. Install Docker Desktop / Docker Engine with Compose.
2. Copy `.env.example` to `.env`; set a strong `DJANGO_SECRET_KEY`. Add `OPENAI_API_KEY` to enable hosted AI.
3. Run:
   ```bash
   docker compose up --build
   ```
4. In another terminal:
   ```bash
   docker compose exec backend python manage.py createsuperuser
   ```
5. Open React at http://localhost:5173 and API at http://localhost:8000/api/v1/health/.

The compose stack runs PostgreSQL with pgvector, Redis, Django/Gunicorn, Celery worker and Vite React frontend. The backend entrypoint applies migrations.

## Local development
Backend:
```bash
cd backend
python -m venv .venv
# activate venv, then:
pip install -r requirements.txt
cp ../.env.example ../.env
python manage.py makemigrations accounts knowledge assistant audit_usage
python manage.py migrate
python manage.py runserver
```
Frontend:
```bash
cd frontend
npm install
npm run dev
```
For local development without PostgreSQL/Redis, configure services in `.env` accordingly; the supported reference deployment is Docker Compose.

## First-use flow
1. Register a user via `POST /api/v1/auth/register/`.
2. Create a workspace via `POST /api/v1/tenants/`.
3. The creator is assigned tenant-admin role.
4. Upload a document at `POST /api/v1/documents/` (multipart field `file`).
5. Wait for processing status `indexed`.
6. Ask questions at `POST /api/v1/chat/ask/` with `{ "tenant_id": 1, "question": "..." }`.
7. Inspect citations returned by the API.

## Important configuration
- `OPENAI_API_KEY`: optional; without it, ingestion uses deterministic local hash embeddings and chat abstains rather than inventing an answer.
- `EMBEDDING_MODEL=text-embedding-3-small`
- `CHAT_MODEL=gpt-4o-mini`
- `MAX_UPLOAD_MB=20`
- `CHUNK_SIZE=900`, `CHUNK_OVERLAP=120`
- Never commit `.env` or production secrets.
- Use HTTPS, managed secrets, encrypted backups, malware scanning and a private object store before real client data.

## API outline
- `POST /api/v1/auth/register/`, `POST /api/v1/auth/login/`, `GET /api/v1/auth/me/`
- `GET/POST /api/v1/tenants/`, `GET/POST /api/v1/members/`
- `GET/POST /api/v1/documents/`, `GET /api/v1/documents/{id}/`
- `POST /api/v1/chat/ask/`, `GET /api/v1/chat/conversations/`
- `POST /api/v1/chat/feedback/`
- `GET /api/v1/health/`

## Tests
```bash
docker compose exec backend python manage.py test
```
The tests cover tenant scoping and core API behavior. Add security regression tests before production use.
